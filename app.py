from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from datetime import datetime
import hashlib
import os
from controllers.led_controller import LedController

from models.database import Database
from models.bloque import Bloque
from models.blockchain import Blockchain
from controllers.bloque_controller import BloqueController
from controllers.blockchain_controller import BlockchainController

app = Flask(__name__)
app.secret_key = os.urandom(24) 

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
            return redirect(url_for('button'))
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
        
        bloque_controller = BloqueController()

        if bloque_controller.usuario_existente(usuario):
            return jsonify({'success': False, 'message': 'El usuario ya está registrado'}), 400

        id = bloque_controller.save(usuario, contrasena)
        
        if id:
            return jsonify({'success': True, 'id': id})
        else:
            return jsonify({'success': False, 'message': 'Error al crear usuario'}), 500
    
    return render_template('usuario/create.html')

#Ruta para mostrar los detalles del usuario creado
@app.route('/usuario/show/<int:id>')
def show(id):
    blockchain_controller = BlockchainController()
    usuario = blockchain_controller.show(id)
    
    if not usuario:
        return redirect(url_for('index'))
    
    return render_template('usuario/show.html', usuario=usuario)

#Ruta para manejar el estado de la luz led en el arduino
@app.route('/usuario/estado_led', methods=['POST'])
def estado_led():
    if 'id_usuario' not in session:
        return jsonify({"success": False, "error": "No hay sesión activa"}), 401
    
    estado = request.form.get('estado')
    
    led_controller = LedController(pin=13)
    result = led_controller.manejar_estado(estado)
    
    if result:
        return jsonify({"success": True}), 200
    else:
        return jsonify({"success": False, "error": "Estado no válido"}), 400

#Ruta para manejar el botón que enciende y apaga el led
@app.route('/usuario/button')
def button():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    
    id_usuario = session.get('id_usuario') 
    return render_template('usuario/button.html', id_usuario=id_usuario)

#Ruta para guardar el estado del botón después de que se interactúa con él
@app.route('/usuario/save_estado', methods=['POST'])
def save_estado():
    if 'id_usuario' not in session:
        return jsonify({"success": False, "error": "No hay sesión activa"}), 401
    
    estado = request.form.get('estado')
    id_usuario = session['id_usuario']
    
    bloque_controller = BloqueController()
    result = bloque_controller.save_estado(id_usuario, estado)
    
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
@app.route('/blockchain/see')
def see_blockchain():
    blockchain_instance = Blockchain()  
    bloques_data = blockchain_instance.see()  
    return render_template('usuario/blockchain.html', bloques=bloques_data)

#Ruta para ver los hashes por aparte del historial
@app.route('/blockchain/block/hash/<hash>')
def see_hash_details(hash):
    blockchain_controller = BlockchainController()
    bloque = blockchain_controller.get_block_by_hash(hash)
    if bloque:
        return render_template('usuario/hash.html', bloque=bloque)
    else:
        return "Bloque no encontrado"

@app.context_processor
def inject_now():
    return {'now': datetime.now()}

if __name__ == '__main__':
    app.run(debug=True)
