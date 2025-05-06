from config.conexion import mysql # Se importan el archivo conexion
import hashlib # Se importan la extencion de el hashlib para simular la creación del blockchain
from datetime import datetime # Se importa la libreria datetime para manejar fechas

# Función para obtener el ultimo hash
def getLastHash():
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = "SELECT hash FROM blockchain ORDER BY id DESC LIMIT 1"
    cursor.execute(sql)
    fila = cursor.fetchone()
    conn.close()
    return fila[0] if fila else "0" # Si no hay hash se cosidera como bloque genesis osea el primer bloque entonces no abria anterio bloque a ese

# Funcion para crear un nuevo usuario
def createUser(usuario, contrasena):
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = "INSERT INTO usuarios (usuario, contrasena) VALUES (%s, %s)"
    cursor.execute(sql, (usuario, contrasena))
    cursor.commit()
    id_usuario = cursor.lastrowid # Aqui obtenemos el id del usuario actual, para usarlo en la función creaateBlock
    conn.close()
    return id_usuario # Retornamos el id del usuario para gestionarlo el la función createBlock

# Se crea un nuevobloque cada vez que se cambie el estado del boton
def createBlock(id_usuario, estado):
    anterior_hash = getLastHash()
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Es el formato de fecha
    datos = fecha + estado + anterior_hash
    resultado = hashlib.sha256(datos.encode()).hexdigest() # Aqui se implementa la libreria hashlib

    conn = mysql.connect()
    cursor = conn.cursor()
    sql = """INSERT INTO blockchain (id_usuario, fecha, estado, anterior_hash, hash)
             VALUES (%s, %s, %s, %s, %s)"""
    cursor.execute(sql, (id_usuario, fecha, estado, anterior_hash, resultado))
    cursor.commit()
    conn.close()
    return True
    