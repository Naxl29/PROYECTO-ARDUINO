from flask import Flask
from flask import render_template, request
from flaskext.mysql import MySQL

app= Flask(__name__)

mysql= MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='dbprueba'
mysql.init_app(app)

@app.route('/')
def index():

    sql ="SELECT * FROM usuarios;"
    conn= mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)
    conn.commit()

    usuarios=cursor.fetchall()
    print(usuarios)

    return render_template('usuarios/index.html')

@app.route('/create')
def create():
    return render_template('usuarios/create.html')

@app.route('/store', methods=['POST'])
def storage():
    _usuario=request.form['usuario']
    _contrasena=request.form['contrasena']

    sql ="INSERT INTO `dbprueba`.`usuarios` (`usuario`, `contrasena`) VALUES (%s, %s);"
    
    datos=(_usuario,_contrasena)

    conn= mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()

    return render_template('usuarios/index.html')

if __name__== '__main__': 
    app.run(debug=True)