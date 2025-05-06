from flask import Flask, render_template, request, redirect, url_for
from conexion import mysql, init_mysql
from Bloque import createUser, createBlock
from Blockchain import see , show

app = Flask(__name__)
init_mysql(app)


@app.route('/')
def index():
    return render_template('usuarios/index.html')

@app.route('/store', methods=['POST'])
def createUser():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contrasena = request.form['contrasena']
        createUser(usuario, contrasena)
        return redirect(url_for('usuarios/button.html'))
    return render_template('usuarios/create.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contrasena = request.form['contrasena']
        user = login(usuario, contrasena)
        if user:
            return redirect(url_for('usuarios/button.html', id_usuario=user['id']))
        else:
            return "Usuario o contraseña incorrectos"
    return render_template('login.html')

@app.route('/bloque/<int:id_usuario>', methods=['POST'])
def createBlock(id_usuario):
    if request.method == 'POST':
        estado = request.form['estado']
        createBlock(id_usuario, estado)
        return redirect(url_for('usuarios/see.html'))
    return render_template('crear_bloque.html', id_usuario=id_usuario)


@app.route('/see')
def see():
    bloques = see()
    return render_template('usuarios/see.html', bloques=bloques)

if __name__ == '__main__':
    app.run(debug=True)
