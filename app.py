from flask import Flask, render_template, request, redirect, url_for # Se importan las dependencias de Flask
from conexion import mysql, init_mysql # Se importa en el archivo de conexxion.py y utilizamos la variable mysql
from Bloque import createUser, createBlock # Se importa del archivo Bloque las funciónes de crear usuario, y crear bloque
from Blockchain import see , show # Se importa el archivo Blockchain las funciones de mostrar usuario creado y el historial

app = Flask(__name__)
init_mysql(app)


@app.route('/')
def index(): # Función para mostrar el index a los usuarios
    return render_template('usuarios/index.html')

# Esta la funcion que toma los datos del formulario de crear usuario
@app.route('/store', methods=['POST']) 
def createUser():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contrasena = request.form['contrasena']
        createUser(usuario, contrasena)
        return redirect(url_for('usuarios/show.html')) # Redirige al usuario recien creado a ver sus datos
    return render_template('usuarios/create.html')

# Toma los datos de formulario de login
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contrasena = request.form['contrasena']
        user = login(usuario, contrasena)
        if user:
            return redirect(url_for('usuarios/button.html', id_usuario=user['id'])) # Redirige al archivo del boton
        else:
            return "Usuario o contraseña incorrectos"
    return render_template('login.html')

# Funcion para mostar el historial
@app.route('/see')
def see():
    bloques = see()
    return render_template('usuarios/see.html', bloques=bloques) #toma los datos del archivo de historial

if __name__ == '__main__':
    app.run(debug=True)
