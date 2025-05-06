from config.conexion import mysql
import hashlib
from datetime import datetime

class Bloque:
    def __init__(self):
        self.conn = None
    # Esta es la misma función de el modelo User para manipular la base de datos
    def conectar(self):
        self.conn = mysql.connect()
        return self.conn.cursor()
    
    # Función para obtener hash anterior 
    def getLastHash(self):
        cursor = self.conectar() # Se usa la conexion
        cursor.execute("SELECT hash FROM blockchain ORDER BY id DESC LIMIT 1")
        fila = cursor.fetchone() # Nos trae la fila de datos de la base de datos
        self.conn.close()
        return fila[0] if fila else "0" # si ya hay bloques creados nos retornara el hash anterior, y si no hay nos traera 0 porque seria el bloque genesis o el primero
    
    # Función para crear un bloque, utilizando el id del los usuarios
    def createBlock(self, id_usuario, estado):
        anterior_hash = self.getlastHash() # Utilizamos la funcion de el hash anterior
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Calculamos la fecha utilizando la libreria datemime
        datos = fecha + estado + anterior_hash # La variable datos contiene la suma de las variables fecha, anterior_hash y estado
        hash_result = hashlib.sha256(datos.encode()).hexdigest() # Esta variable es la que generara el hash del bloque creado utilizando la libreria hashlib

        cursor = self.conectar()
        sql = """
            INSERT INTO blockchain (id_usuario, fecha, estado, anterior_hash, hash)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (id_usuario, fecha, estado, anterior_hash, hash_result))
        self.conn.commit()
        self.conn.close()
        return True
    
    # Función que se utilizara para mostar el historial
    def see(self):
        conn = self.conectar() # Se usa al conexion
        cursor = conn.cursor(dictionary=True)  # Retorna cada fila como un diccionario
        sql = """
            SELECT b.id, u.usuario, b.fecha, b.estado, b.anterior_hash, b.hash
            FROM blockchain b
            JOIN usuarios u ON b.id_usuario = u.id
            ORDER BY b.id ASC
        """
        cursor.execute(sql)
        bloques = cursor.fetchall() # Aqui traemos todas las filas que hay en la base de datos
        conn.close()

        return bloques # Retornamos toda la información de los usuarios
