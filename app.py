from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from datetime import datetime
import os

# Controladores
from Controller.led_controller import LedController
from Controller.ml_controller import MLController
from Controller.dashboard_controller import DashboardController
from Controller.bloque_controller import BloqueController
from Controller.reporte_controller import ReporteController
from Controller.led_device_controller import LedDeviceController

# Configuración y utilidades
from config.roles_config import ROLES, LED_NAMES
from utils.auth_utils import can_control_led, get_role_info, check_session, get_user_info
from utils.leds_store import get_led_names, save_led_name

app = Flask(__name__)
app.secret_key = os.urandom(24) 

led_controller = None
led_device_controller = None

def get_led_controller():
    global led_controller
    if led_controller is None:
        led_controller = LedController()
    return led_controller

def get_led_device_controller():
    global led_device_controller
    if led_device_controller is None:
        led_device_controller = LedDeviceController()
    return led_device_controller


@app.route('/')
def index():
    return render_template('index.html')

#Ruta para iniciar sesión con un usuario ya registrado
@app.route('/usuario/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contrasena = request.form['contrasena']
        
        bloque_controller = BloqueController()
        user = bloque_controller.login(usuario, contrasena) 
        
        if user:
            session['usuario'] = user['usuario']
            session['id_usuario'] = user['id']
            session['rol'] = user['rol'] if user['rol'] else 'USER'
            return redirect(url_for('dashboard'))
        else:
            error_message = 'Usuario o contraseña incorrecta'
            return render_template('usuario/login.html', error_message=error_message)
    
    return render_template('usuario/login.html')

#Ruta para crear y registrar un nuevo usuario
@app.route('/usuario/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contrasena = request.form['contrasena']
        
        # Validar que los campos no estén vacíos
        if not usuario.strip() or not contrasena.strip():
            return jsonify({'success': False, 'message': 'Todos los campos son obligatorios'}), 400
        
        bloque_controller = BloqueController()

        if bloque_controller.usuario_existente(usuario):
            return jsonify({'success': False, 'message': 'El usuario ya está registrado'}), 400
        try:
            id = bloque_controller.save(usuario, contrasena)
            
            if id:
                return jsonify({'success': True, 'message': 'Usuario creado correctamente', 'id': id}), 201
            else:
                return jsonify({'success': False, 'message': 'Error al crear usuario'}), 500
                
        except Exception as e:
            return jsonify({'success': False, 'message': 'Error al crear usuario - posiblemente ya existe'}), 409
    
    return render_template('usuario/create.html')

#Ruta para mostrar los detalles del usuario creado
@app.route('/usuario/show/<int:id>')
def show(id):
    reporte_controller = ReporteController()
    usuario = reporte_controller.show(id)
    
    if not usuario:
        return redirect(url_for('index'))
    
    return render_template('usuario/show.html', usuario=usuario)

#Ruta para manejar el estado de la luz led en el arduino
@app.route('/usuario/estado_led', methods=['POST'])
def estado_led():
    if not check_session():
        return jsonify({"success": False, "error": "No hay sesión activa"}), 401

    estado = request.form.get('estado')  # '1' o '0'
    led_id = request.form.get('led_id')  # '1', '2', '3', '4','5', '6', '7', '8'o 'ALL'
    user_info = get_user_info()
    user_role = user_info['rol']

    static_allowed = ['1', '2', '3', '4', '5', '6', '7', '8', 'ALL']
    if not led_id:
        return jsonify({"success": False, "error": "LED ID inválido"}), 400
    is_dynamic_numeric = led_id.isdigit() and led_id not in static_allowed
    if (led_id not in static_allowed) and (not is_dynamic_numeric):
        return jsonify({"success": False, "error": "LED ID inválido"}), 400

    # Verificar permisos según el rol del usuario
    if (led_id in static_allowed) and (not can_control_led(led_id, user_role)):
        return jsonify({"success": False, "error": "No tienes permisos para controlar este dispositivo"}), 403
    # Para dinámicos, permitir control a cualquier rol autenticado (ADMIN/USER/CHILD)

    if led_id in static_allowed:
        result = get_led_controller().manejar_estado(estado, led_id)
    else:
        # dinámico
        result = get_led_device_controller().send_state(led_id, estado)

    if result:
        return jsonify({"success": True}), 200
    else:
        return jsonify({"success": False, "error": "Error al controlar LED"}), 500

#Ruta para manejar el botón que enciende y apaga el led
@app.route('/usuario/button')
def button():
    if not check_session():
        return redirect(url_for('login'))
    
    user_info = get_user_info()
    user_role = user_info['rol']
    
    # Merge custom LED names with defaults
    dynamic_led_names = get_led_names(LED_NAMES)
    # Dispositivos dinámicos desde DB
    devices = get_led_device_controller().list_devices()
    return render_template('usuario/button.html', 
                         id_usuario=user_info['id_usuario'], 
                         user_role=user_role,
                         led_names=dynamic_led_names,
                         devices=devices,
                         role_config=ROLES.get(user_role, ROLES['USER']))

#Ruta para guardar el estado del botón después de que se interactúa con él
@app.route('/usuario/save_estado', methods=['POST'])
def save_estado():
    if not check_session():
        return jsonify({"success": False, "error": "No hay sesión activa"}), 401
    
    estado = request.form.get('estado')
    led_id = request.form.get('led_id')
    user_info = get_user_info()
    
    bloque_controller = BloqueController()
    result = bloque_controller.save_estado(user_info['id_usuario'], estado, led_id)
    
    if result:
        return jsonify({"success": True}), 200
    else:
        return jsonify({"success": False, "error": "Error al guardar"}), 500

# Admin: formulario para crear nuevo LED (DB)
@app.route('/admin/devices/new', methods=['GET', 'POST'])
def admin_new_device():
    if not check_session():
        return redirect(url_for('login'))

    user_info = get_user_info()
    if user_info['rol'] != 'ADMIN':
        flash('No tienes permisos para acceder a esta función', 'error')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        nombre = (request.form.get('nombre') or '').strip()
        potencia = float(request.form.get('potencia') or 0)
        consumo = float(request.form.get('consumo') or 0)
        color = (request.form.get('color') or '#ffffff').strip()

        if not nombre:
            flash('El nombre es obligatorio', 'error')
            return redirect(url_for('admin_new_device'))

        try:
            assigned_channel = get_led_device_controller().create_device(nombre, potencia, consumo, color)
            flash(f'Dispositivo creado correctamente (canal {assigned_channel})', 'success')
            # Permanecer en la misma página (GET) para poder seguir agregando más
            return redirect(url_for('admin_new_device'))
        except Exception as e:
            flash(f'Error al crear dispositivo: {e}', 'error')
            return redirect(url_for('admin_new_device'))

    ldc = get_led_device_controller()
    existing_dynamic = ldc.list_devices()
    base_leds = ldc.list_base_leds()
    # Merge for list view: show base first, then dynamic
    all_for_list = base_leds + existing_dynamic
    return render_template('admin/new_device.html', devices=all_for_list)

# Ruta para obtener todos los estados de los LEDs
@app.route('/led/get_estados', methods=['GET'])
def get_estados():
    if not check_session():
        return jsonify({"success": False, "error": "No hay sesión activa"}), 401
    
    user_info = get_user_info()
    bloque_controller = BloqueController()
    
    # Obtener el último estado de cada LED para este usuario
    estados = bloque_controller.get_current_states(user_info['id_usuario'])
    
    if estados is not None:
        return jsonify({"success": True, "estados": estados}), 200
    else:
        return jsonify({"success": False, "error": "Error al obtener estados"}), 500

#Ruta para cerrar sesión
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

#Ruta para el historial de interacciones con el botón
@app.route('/blockchain/block')
def see_blockchain():
    if not check_session():
        return redirect(url_for('login'))
    
    user_info = get_user_info()
    
    reporte_controller = ReporteController()
    bloques, total_gasto = reporte_controller.see(user_info['id_usuario'], user_info['rol'])

    return render_template('usuario/reporte.html', bloques=bloques, total_gasto=total_gasto, user_role=user_info['rol'])

#Esta ruta no se utilizará en la nueva actualización
#Ruta para ver los hashes por aparte del historial
@app.route('/blockchain/block/hash/<hash>')
def see_hash_details(hash):
    reporte_controller = ReporteController()
    bloque = reporte_controller.get_block_by_hash(hash)
    if bloque:
        return render_template('usuario/hash.html', bloque=bloque)
    else:
        return "Bloque no encontrado"

@app.route('/usuario/dashboard')
def dashboard():
    if not check_session():
        return redirect(url_for('login'))
    
    user_info = get_user_info()
    user_role = user_info['rol']
    role_info = get_role_info(user_role)
    
    dashboard_controller = DashboardController()
    stats = dashboard_controller.get_dashboard_stats(user_role)
    
    if not stats:
        flash('Error al cargar el dashboard', 'error')
        return redirect(url_for('index'))
    
    stats['role_info'] = role_info
    # Provide dynamic names for any widgets that may need them
    stats['led_names'] = get_led_names(LED_NAMES)
    return render_template('usuario/dashboard.html', **stats)

# Admin: agregar/renombrar LED (nombre amigable)
@app.route('/admin/leds/new', methods=['GET', 'POST'])
def admin_add_led():
    if not check_session():
        return redirect(url_for('login'))

    user_info = get_user_info()
    if user_info['rol'] != 'ADMIN':
        flash('No tienes permisos para acceder a esta función', 'error')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        led_id = request.form.get('led_id', '').strip()
        name = request.form.get('name', '').strip()

        if not led_id or not name:
            flash('Todos los campos son obligatorios', 'error')
            return redirect(url_for('admin_add_led'))

        ok = save_led_name(led_id, name)
        if not ok:
            flash('LED inválido (usa 1..8) o nombre vacío', 'error')
            return redirect(url_for('admin_add_led'))

        flash(f'LED {led_id} actualizado a "{name}"', 'success')
        return redirect(url_for('button'))

    # GET
    current_names = get_led_names(LED_NAMES)
    return render_template('admin/add_led.html', led_names=current_names, roles=ROLES)

@app.context_processor
def inject_now():
    return {'now': datetime.now()}

@app.route('/ml/prediccion_mensual')
def prediccion_mensual():
    """Ruta para obtener la predicción del recibo mensual"""
    if not check_session():
        return jsonify({'error': 'No autorizado'}), 401
    
    try:
        ml_controller = MLController()
        prediccion = ml_controller.predecir_recibo_mensual()
        return jsonify(prediccion)
    except Exception as e:
        return jsonify({'error': str(e), 'exitoso': False}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
