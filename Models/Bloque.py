from datetime import datetime
import hashlib
from models.database import Database

class Bloque:
    def __init__(self):
        self.db = Database()
    
    
    #Obtiene el último hash para agregarlo al historial
    def obtener_ultimo_hash(self):
        conn = self.db.conexion()
        cursor = conn.cursor(dictionary=True)
        
        sql = "SELECT hash FROM blockchain ORDER BY id DESC LIMIT 1"
        cursor.execute(sql)
        fila = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return fila['hash'] if fila else '0'
    
    #Función para crear un nuevo usuario
    def create_user(self, usuario, contrasena):
        if self.usuario_existe(usuario):
            return "Usuario ya registrado"
        
        conn = self.db.conexion()
        cursor = conn.cursor()
        
        sql = "INSERT INTO usuarios (usuario, contrasena) VALUES (%s, %s)"
        cursor.execute(sql, (usuario, contrasena))
        conn.commit()
        
        last_id = cursor.lastrowid
        
        cursor.close()
        conn.close()
        
        return last_id if cursor.rowcount > 0 else False

    #Función para crear un nuevo registro al interactuar con el botón
    def create_blo(self, id_usuario, estado):
        anterior_hash = self.obtener_ultimo_hash()
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        datos = fecha + estado + anterior_hash
        hash_value = hashlib.sha256(datos.encode()).hexdigest()
        
        conn = self.db.conexion()
        cursor = conn.cursor()
        
        sql = """INSERT INTO blockchain (id_usuario, fecha, estado, anterior_hash, hash)
                VALUES (%s, %s, %s, %s, %s)"""
        cursor.execute(sql, (id_usuario, fecha, estado, anterior_hash, hash_value))
        conn.commit()
        
        result = cursor.rowcount > 0
        
        cursor.close()
        conn.close()
        
        return result
    
    #Función para iniciar sesión
    def login(self, usuario, contrasena):
        conn = self.db.conexion()
        cursor = conn.cursor(dictionary=True)
        
        sql = "SELECT * FROM usuarios WHERE usuario = %s AND contrasena = %s"
        cursor.execute(sql, (usuario, contrasena))
        user = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return user
    
    #Función para verificar la contraseña del usuario 
    def password_veri(self, usuario, contrasena):
        conn = self.db.conexion()
        cursor = conn.cursor(dictionary=True)
        
        sql = "SELECT contrasena FROM usuarios WHERE usuario = %s"
        cursor.execute(sql, (usuario,))
        user = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if user and contrasena == user['contrasena']:
            return True
        return False
    
    #Función que verifica que el nombre de usuario no exista en la base de datos
    def usuario_existe(self, usuario):
        conn = self.db.conexion()
        cursor = conn.cursor(dictionary=True, buffered=True)
        
        sql = "SELECT id FROM usuarios WHERE usuario = %s"
        cursor.execute(sql, (usuario,))
        resultado = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return resultado is not None
