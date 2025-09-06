from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from datetime import datetime
import hashlib
import os
from functools import wraps
from Controller.led_controller import LedController
from Controller.ml_controller import MLController
from config.roles_config import ROLES, LED_NAMES

from Model.database import Database
from Model.bloque import Bloque
from Model.reporte import Reporte
from Controller.bloque_controller import BloqueController
from Controller.reporte_controller import ReporteController

app = Flask(__name__)
app.secret_key = os.urandom(24) 

led_controller = None

def get_led_controller():
    global led_controller
    if led_controller is None:
        led_controller = LedController()
    return led_controller


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
    if 'id_usuario' not in session:
        return jsonify({"success": False, "error": "No hay sesión activa"}), 401

    estado = request.form.get('estado')  # '1' o '0'
    led_id = request.form.get('led_id')  # '1', '2', '3', '4','5', '6', '7', '8'o 'ALL'
    user_role = session.get('rol', 'USER')

    if not led_id or led_id not in ['1', '2', '3', '4', '5', '6', '7', '8', 'ALL']:
        return jsonify({"success": False, "error": "LED ID inválido"}), 400

    # Verificar permisos según el rol del usuario
    if not can_control_led(led_id, user_role):
        return jsonify({"success": False, "error": "No tienes permisos para controlar este dispositivo"}), 403

    result = get_led_controller().manejar_estado(estado, led_id)

    if result:
        return jsonify({"success": True}), 200
    else:
        return jsonify({"success": False, "error": "Error al controlar LED"}), 500

#Ruta para manejar el botón que enciende y apaga el led
@app.route('/usuario/button')
def button():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    
    id_usuario = session.get('id_usuario')
    user_role = session.get('rol', 'USER')
    
    return render_template('usuario/button.html', 
                         id_usuario=id_usuario, 
                         user_role=user_role,
                         led_names=LED_NAMES,
                         role_config=ROLES.get(user_role, ROLES['USER']))

#Ruta para guardar el estado del botón después de que se interactúa con él
@app.route('/usuario/save_estado', methods=['POST'])
def save_estado():
    if 'id_usuario' not in session:
        return jsonify({"success": False, "error": "No hay sesión activa"}), 401
    
    estado = request.form.get('estado')
    led_id = request.form.get('led_id')
    id_usuario = session['id_usuario']
    
    bloque_controller = BloqueController()
    result = bloque_controller.save_estado(id_usuario, estado, led_id)
    
    if result:
        return jsonify({"success": True}), 200
    else:
        return jsonify({"success": False, "error": "Error al guardar"}), 500

#Ruta para cerrar sesión
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

#Ruta para el historial de interacciones con el botón
@app.route('/blockchain/block')
def see_blockchain():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    
    id_usuario = session.get('id_usuario')
    user_role = session.get('rol', 'USER')
    
    reporte_controller = ReporteController()
    bloques, total_gasto = reporte_controller.see(id_usuario, user_role)

    return render_template('usuario/reporte.html', bloques=bloques, total_gasto=total_gasto, user_role=user_role)

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
    if 'usuario' not in session:
        return redirect(url_for('login'))
    
    user_role = session.get('rol', 'USER')
    role_info = get_role_info(user_role)
    
    db = Database()
    conn = db.conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) AS total_usuarios FROM usuarios")
    total_usuarios = cursor.fetchone()['total_usuarios']

    cursor.execute("SELECT COUNT(*) AS total_encendidos FROM reportes WHERE estado = 1")
    total_encendidos = cursor.fetchone()['total_encendidos']

    cursor.execute("""
        SELECT u.usuario, b.fecha
        FROM reportes b
        JOIN usuarios u on b.id_usuario = u.id
        WHERE b.estado = 1
        ORDER BY b.fecha DESC
        LIMIT 5
    """
    )
    ultimos_encendidos = cursor.fetchall()

    cursor.execute("""
        SELECT DATE(fecha) as fecha, COUNT(*) as cantidad
        FROM reportes
        WHERE estado = 1
        GROUP BY fecha
        ORDER BY fecha ASC
    """)
    grafico_data = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'usuario/dashboard.html',
        total_usuarios=total_usuarios,
        total_encendidos=total_encendidos,
        ultimos_encendidos=ultimos_encendidos,
        grafico_data=grafico_data,
        user_role=user_role,
        role_info=role_info
    )

@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# Decorador para verificar permisos
def require_role(allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'id_usuario' not in session:
                return redirect(url_for('login'))
            
            user_role = session.get('rol', 'USER')
            if user_role not in allowed_roles:
                flash('No tienes permisos para acceder a esta función', 'error')
                return redirect(url_for('dashboard'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Función para verificar permisos de LED
def can_control_led(led_id, user_role):
    """
    Verifica si un usuario puede controlar un LED específico según su rol
    """
    if user_role not in ROLES:
        return False
    
    allowed_leds = ROLES[user_role]['permissions']['accessible_leds']
    return led_id in allowed_leds

# Función para obtener información del rol
def get_role_info(user_role):
    """
    Obtiene la información completa del rol del usuario
    """
    return ROLES.get(user_role, ROLES['USER'])

# Función para obtener nombre del LED
def get_led_name(led_id):
    """
    Obtiene el nombre descriptivo de un LED
    """
    return LED_NAMES.get(led_id, f'LED {led_id}')


@app.route('/ml/prediccion_mensual')
def prediccion_mensual():
    """Ruta para obtener la predicción del recibo mensual"""
    if 'id_usuario' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    
    try:
        ml_controller = MLController()
        prediccion = ml_controller.predecir_recibo_mensual()
        return jsonify(prediccion)
    except Exception as e:
        return jsonify({'error': str(e), 'exitoso': False}), 500

if __name__ == '__main__':
    app.run(debug=True)
