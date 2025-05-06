from flask import Flask
from flask import render_template, request
from flaskext.mysql import MySQL

app= Flask(__name__)

#conexión con la base de datos
mysql= MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='blockchain'
mysql.init_app(app)

#Función para mostrar todos los registros
@app.route('/')
def index():

    sql ="SELECT * FROM blockchain;"
    conn= mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)
    conn.commit()

    blockchain=cursor.fetchall()
    print(blockchain)

    return render_template('usuarios/index.html', blockchain=blockchain)

#Función para crear nuevos usuarios
@app.route('/create')
def create():
    return render_template('usuarios/create.html')

#Función para almacenar y guardar los datos introducidos en el formulario de crear usuario
@app.route('/store', methods=['POST'])
def storage():
    _usuario=request.form['usuario']
    _contrasena=request.form['contrasena']

    sql ="INSERT INTO `blockchain`.`usuarios` (`usuario`, `contrasena`) VALUES (%s, %s);"
    
    datos=(_usuario,_contrasena)

    conn= mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()

    return render_template('usuarios/index.html')

if __name__== '__main__': 
    app.run(debug=True)