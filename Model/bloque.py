from datetime import datetime
import hashlib
from Model.database import Database

class Bloque:
    def __init__(self):
        self.db = Database()
    
    #Se omitirá esto por el momento para la actualización del proyecto
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
        # Verificar si el usuario ya existe
        if self.usuario_existe(usuario):
            return False  # o lanzar una excepción específica
        
        conn = self.db.conexion()
        cursor = conn.cursor()
        
        try:
            sql = "INSERT INTO usuarios (usuario, contrasena) VALUES (%s, %s)"
            cursor.execute(sql, (usuario, contrasena))
            conn.commit()
            
            last_id = cursor.lastrowid
            return last_id if cursor.rowcount > 0 else False
            
        except Exception as e:
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    #Función para crear un nuevo registro al interactuar con el botón
    def create_blo(self, id_usuario, id_objeto, duracion, estado, gasto):
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        conn = self.db.conexion()
        cursor = conn.cursor()
        
        sql = """INSERT INTO reportes (id_usuario, id_objeto, fecha, duracion_minutos, estado, gasto)
                VALUES (%s, %s, %s, %s, %s, %s)"""
        cursor.execute(sql, (id_usuario, id_objeto, fecha, duracion, estado, gasto))
        conn.commit()
        
        result = cursor.rowcount > 0
        
        cursor.close()
        conn.close()
        
        return result
    
    #Función para iniciar sesión
    def login(self, usuario, contrasena):
        conn = self.db.conexion()
        cursor = conn.cursor(dictionary=True)
        
        try:
            # Intentar con la consulta que incluye roles
            sql = """
                SELECT u.*, r.rol 
                FROM usuarios u
                LEFT JOIN roles_usuarios ru ON u.id = ru.id_usuario
                LEFT JOIN roles r ON ru.id_rol = r.id
                WHERE u.usuario = %s AND u.contrasena = %s
            """
            cursor.execute(sql, (usuario, contrasena))
            user = cursor.fetchone()
            
        except Exception as e:
            # Si las tablas de roles no existen, usar consulta simple
            print(f"Error con roles, usando consulta simple: {e}")
            sql = "SELECT *, 'USER' as rol FROM usuarios WHERE usuario = %s AND contrasena = %s"
            cursor.execute(sql, (usuario, contrasena))
            user = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return user
    
    #Función para obtener el rol del usuario
    def get_user_role(self, id_usuario):
        conn = self.db.conexion()
        cursor = conn.cursor(dictionary=True)
        
        try:
            sql = """
                SELECT r.rol 
                FROM roles r
                JOIN roles_usuarios ru ON r.id = ru.id_rol
                WHERE ru.id_usuario = %s
            """
            cursor.execute(sql, (id_usuario,))
            result = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            return result['rol'] if result else 'USER'
            
        except Exception as e:
            print(f"Error obteniendo rol: {e}")
            cursor.close()
            conn.close()
            return 'USER'
    
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
