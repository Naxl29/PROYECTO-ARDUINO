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
from Controller.section_controller import SectionController
from Model.database import Database  # Import necesario para operaciones directas en DB (eliminación de dispositivos)

# Configuración y utilidades
from config.roles_config import ROLES, LED_NAMES
from utils.auth_utils import can_control_led, get_role_info, check_session, get_user_info
from utils.leds_store import get_led_names, save_led_name
from Model.device_flags import DeviceFlagsModel

# Inicialización de base de datos
from Model.init_db import DatabaseInitializer

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Inicializar base de datos al arrancar la aplicación
print("🚀 Iniciando aplicación...")
DatabaseInitializer.initialize_all_tables()
DatabaseInitializer.insert_default_data() 

led_controller = None
led_device_controller = None
section_controller = None

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

def get_section_controller():
    global section_controller
    if section_controller is None:
        section_controller = SectionController()
    return section_controller


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
    # Verificación adicional: permisos por sección (si aplica)
    if led_id != 'ALL':
        try:
            sec_map = get_section_controller().sections_map()
            sec = sec_map.get(str(led_id))
            if sec and sec.get('roles'):
                if user_role not in sec['roles']:
                    return jsonify({"success": False, "error": "No tienes permiso para esta sección"}), 403
        except Exception:
            pass
    # Para dinámicos, permitir control a cualquier rol autenticado (ADMIN/USER/CHILD) si no hay restricción de sección

    # Bloqueo por suspensión de canal (estático o dinámico)
    try:
        if led_id != 'ALL' and DeviceFlagsModel.is_suspended(led_id):
            return jsonify({"success": False, "error": "Este dispositivo está suspendido"}), 423
    except Exception:
        pass

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
    # Secciones para filtro y mapeo canal->sección
    sections = get_section_controller().list_sections()
    sections_map = get_section_controller().sections_map()
    flags_map = DeviceFlagsModel.get_flags_map()
    return render_template('usuario/button.html', 
                         id_usuario=user_info['id_usuario'], 
                         user_role=user_role,
                         led_names=dynamic_led_names,
                         devices=devices,
                         sections=sections,
                         sections_map=sections_map,
                         flags_map=flags_map,
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
        section_id = request.form.get('section_id')

        if not nombre:
            flash('El nombre es obligatorio', 'error')
            return redirect(url_for('admin_new_device'))

        try:
            assigned_channel = get_led_device_controller().create_device(nombre, potencia, consumo, color)
            # Asignación opcional de sección
            try:
                if section_id and str(section_id).isdigit():
                    get_section_controller().assign_device(assigned_channel, int(section_id))
            except Exception as _:
                pass
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
    # Secciones disponibles
    sections = get_section_controller().list_sections()
    sections_map = get_section_controller().sections_map()
    flags_map = DeviceFlagsModel.get_flags_map()
    return render_template('admin/new_device.html', devices=all_for_list, sections=sections, sections_map=sections_map, flags_map=flags_map)

# Admin: asignar/quitar sección a un canal
@app.route('/admin/sections/assign', methods=['POST'])
def admin_assign_section():
    if not check_session():
        return redirect(url_for('login'))
    user_info = get_user_info()
    if user_info['rol'] != 'ADMIN':
        flash('No tienes permisos para acceder a esta función', 'error')
        return redirect(url_for('dashboard'))

    channel = (request.form.get('channel') or '').strip()
    section_id = (request.form.get('section_id') or '').strip()
    try:
        if section_id and section_id.isdigit():
            get_section_controller().assign_device(channel, int(section_id))
            flash('Sección asignada correctamente', 'success')
        else:
            get_section_controller().unassign_device(channel)
            flash('Sección eliminada del dispositivo', 'success')
    except Exception as e:
        flash(f'Error al actualizar sección: {e}', 'error')
    return redirect(url_for('admin_new_device'))

# Admin: crear y listar secciones
@app.route('/admin/sections', methods=['GET', 'POST'])
def admin_sections():
    if not check_session():
        return redirect(url_for('login'))

    user_info = get_user_info()
    if user_info['rol'] != 'ADMIN':
        flash('No tienes permisos para acceder a esta función', 'error')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        nombre = (request.form.get('nombre') or '').strip()
        roles = request.form.getlist('roles')  # ['ADMIN','USER',...]
        if not nombre:
            flash('El nombre de la sección es obligatorio', 'error')
            return redirect(url_for('admin_sections'))
        try:
            new_id = get_section_controller().create_section(nombre)
            # set roles si se enviaron
            try:
                if roles:
                    get_section_controller().set_section_roles(new_id, roles)
            except Exception:
                pass
            flash('Sección creada correctamente', 'success')
        except Exception as e:
            flash(f'Error al crear sección: {e}', 'error')
        return redirect(url_for('admin_sections'))

    sections = get_section_controller().list_sections_with_roles()
    available_roles = list(ROLES.keys())
    return render_template('admin/sections.html', sections=sections, available_roles=available_roles)

# Admin: actualizar sección (nombre y roles)
@app.route('/admin/sections/update', methods=['POST'])
def admin_sections_update():
    if not check_session():
        return redirect(url_for('login'))

    user_info = get_user_info()
    if user_info['rol'] != 'ADMIN':
        flash('No tienes permisos para acceder a esta función', 'error')
        return redirect(url_for('dashboard'))

    section_id = request.form.get('section_id', '').strip()
    nombre = (request.form.get('nombre') or '').strip()
    roles = request.form.getlist('roles')
    if not section_id.isdigit():
        flash('ID de sección inválido', 'error')
        return redirect(url_for('admin_sections'))
    try:
        if nombre:
            get_section_controller().update_section(int(section_id), nombre)
        # actualizar roles (pueden ser vacíos para dejar sin restricciones)
        get_section_controller().set_section_roles(int(section_id), roles)
        flash('Sección actualizada', 'success')
    except Exception as e:
        flash(f'Error al actualizar sección: {e}', 'error')
    return redirect(url_for('admin_sections'))

# Admin: suspender/activar sección
@app.route('/admin/sections/suspend', methods=['POST'])
def admin_sections_suspend():
    if not check_session():
        return redirect(url_for('login'))

    user_info = get_user_info()
    if user_info['rol'] != 'ADMIN':
        flash('No tienes permisos para acceder a esta función', 'error')
        return redirect(url_for('dashboard'))

    section_id = (request.form.get('section_id') or '').strip()
    suspend = (request.form.get('suspend') or '0') == '1'
    if not section_id.isdigit():
        flash('ID de sección inválido', 'error')
        return redirect(url_for('admin_sections'))
    try:
        get_section_controller().suspender_seccion(int(section_id), suspend)
        flash('Sección actualizada', 'success')
    except Exception as e:
        flash(f'Error al actualizar sección: {e}', 'error')
    return redirect(url_for('admin_sections'))

# Admin: eliminar sección
@app.route('/admin/sections/delete', methods=['POST'])
def admin_sections_delete():
    if not check_session():
        return redirect(url_for('login'))

    user_info = get_user_info()
    if user_info['rol'] != 'ADMIN':
        flash('No tienes permisos para acceder a esta función', 'error')
        return redirect(url_for('dashboard'))

    section_id = (request.form.get('section_id') or '').strip()
    if not section_id.isdigit():
        flash('ID de sección inválido', 'error')
        return redirect(url_for('admin_sections'))
    try:
        get_section_controller().eliminar_seccion(int(section_id))
        flash('Sección eliminada', 'success')
    except Exception as e:
        flash(f'Error al eliminar sección: {e}', 'error')
    return redirect(url_for('admin_sections'))

# Admin: suspender/activar LED (canal)
@app.route('/admin/devices/suspend', methods=['POST'])
def admin_devices_suspend():
    if not check_session():
        return redirect(url_for('login'))

    user_info = get_user_info()
    if user_info['rol'] != 'ADMIN':
        flash('No tienes permisos para acceder a esta función', 'error')
        return redirect(url_for('dashboard'))

    channel = (request.form.get('channel') or '').strip()
    suspend = (request.form.get('suspend') or '0') == '1'
    if not channel:
        flash('Canal inválido', 'error')
        return redirect(url_for('admin_new_device'))
    try:
        DeviceFlagsModel.set_suspended(channel, suspend)
        flash('Dispositivo actualizado', 'success')
    except Exception as e:
        flash(f'Error al actualizar dispositivo: {e}', 'error')
    return redirect(url_for('admin_new_device'))

# Admin: editar LED/dispositivo
@app.route('/admin/devices/edit', methods=['POST'])
def admin_devices_edit():
    if not check_session():
        return redirect(url_for('login'))

    user_info = get_user_info()
    if user_info['rol'] != 'ADMIN':
        flash('No tienes permisos para acceder a esta función', 'error')
        return redirect(url_for('dashboard'))

    channel = (request.form.get('channel') or '').strip()
    nombre = (request.form.get('nombre') or '').strip()
    potencia = float(request.form.get('potencia') or 0)
    consumo = float(request.form.get('consumo') or 0)
    color = (request.form.get('color') or '#ffffff').strip()

    if not channel or not nombre:
        flash('Canal y nombre son obligatorios', 'error')
        return redirect(url_for('admin_new_device'))

    try:
        get_led_device_controller().update_device(channel, nombre, potencia, consumo, color)
        flash('Dispositivo actualizado correctamente', 'success')
    except Exception as e:
        flash(f'Error al actualizar dispositivo: {e}', 'error')
    return redirect(url_for('admin_new_device'))

# Admin: eliminar LED dinámico (de DB) y limpiar flags/assignments
@app.route('/admin/devices/delete', methods=['POST'])
def admin_devices_delete():
    if not check_session():
        return redirect(url_for('login'))

    user_info = get_user_info()
    if user_info['rol'] != 'ADMIN':
        flash('No tienes permisos para acceder a esta función', 'error')
        return redirect(url_for('dashboard'))

    channel = (request.form.get('channel') or '').strip()
    if not channel or not channel.isdigit() or int(channel) <= 8:
        flash('Solo se pueden eliminar dispositivos dinámicos (canal >= 9)', 'error')
        return redirect(url_for('admin_new_device'))
    # Usar el modelo unificado para borrar y limpiar dependencias
    try:
        get_led_device_controller().delete_device(channel)
        flash('Dispositivo eliminado', 'success')
    except Exception as e:
        flash(f'Error al eliminar dispositivo: {e}', 'error')
    return redirect(url_for('admin_new_device'))

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
