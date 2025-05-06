from conexion import mysql
import hashlib
from datetime import datetime

def getLastHash():
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = "SELECT hash FROM blockchain ORDER BY id DESC LIMIT 1"
    cursor.execute(sql)
    fila = cursor.fetchone()
    conn.close()
    return fila[0] if fila else "0"

def createUser(usuario, contrasena):
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = "INSERT INTO usuarios (usuario, contrasena) VALUES (%s, %s)"
    cursor.execute(sql, (usuario, contrasena))
    cursor.commit()
    id_usuario = cursor.lastrowid
    conn.close()
    return id_usuario

def createBlock(id_usuario, estado):
    anterior_hash = getLastHash()
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    datos = fecha + estado + anterior_hash
    resultado = hashlib.sha256(datos.encode()).hexdigest()

    conn = mysql.connect()
    cursor = conn.cursor()
    sql = """INSERT INTO blockchain (id_usuario, fecha, estado, anterior_hash, hash)
             VALUES (%s, %s, %s, %s, %s)"""
    cursor.execute(sql, (id_usuario, fecha, estado, anterior_hash, resultado))
    cursor.commit()
    conn.close()
    return True
    