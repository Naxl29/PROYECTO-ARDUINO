from datetime import datetime
from typing import Dict, List, Optional, Tuple

from Model.database import Database

class Bloque:
    def __init__(self):
        self.db = Database()
    
    #Se omitirá esto por el momento para la actualización del proyecto
    #Obtiene el último hash para agregarlo al historial
    def obtener_ultimo_hash(self):
        conn = self.db.conexion()
        cursor = conn.cursor()
        
        sql = "SELECT hash FROM reportes ORDER BY id DESC LIMIT 1"
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
        cursor = conn.cursor()
        
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
        cursor = conn.cursor()
        
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
        cursor = conn.cursor()
        
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
        cursor = conn.cursor()
        
        sql = "SELECT id FROM usuarios WHERE usuario = %s"
        cursor.execute(sql, (usuario,))
        resultado = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return resultado is not None
    
    #Función para obtener información del objeto (potencia y consumo)
    def get_objeto_info(self, id_objeto):
        conn = self.db.conexion()
        cursor = conn.cursor()
        
        sql = "SELECT objeto, potencia_w, consumo_wh FROM objetos WHERE id = %s"
        cursor.execute(sql, (id_objeto,))
        resultado = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return resultado
    
    #Función para calcular la duración real de uso entre encendido y apagado
    def calcular_duracion(self, id_usuario, id_objeto):
        conn = self.db.conexion()
        cursor = conn.cursor()
        
        # Buscar el último registro de encendido (estado = 1) para este usuario y objeto
        sql = """
            SELECT fecha FROM reportes 
            WHERE id_usuario = %s AND id_objeto = %s AND estado = 1 
            ORDER BY fecha DESC LIMIT 1
        """
        cursor.execute(sql, (id_usuario, id_objeto))
        ultimo_encendido = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if ultimo_encendido:
            fecha_encendido = ultimo_encendido['fecha']
            fecha_actual = datetime.now()
            
            # Diferencia real en segundos
            diferencia_segundos = (fecha_actual - fecha_encendido).total_seconds()

             # Simulación: cada segundo equivale a 10 minutos
            duracion_minutos = diferencia_segundos * 10
            
            return round(duracion_minutos, 2)  # Redondear a 2 decimales
        
        return 0.0  # Si no hay registro de encendido previo

    #Función para obtener todos los objetos de la tabla
    def get_all_objetos(self):
        conn = self.db.conexion()
        cursor = conn.cursor()
        
        sql = "SELECT id, objeto, potencia_w, consumo_wh FROM objetos"
        cursor.execute(sql)
        resultados = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return resultados

    # Función para calcular el gasto en base a consumo y duración
    def calcular_gasto(self, id_objeto, duracion_minutos, tarifa_cop_kwh=1000):
        objeto_info = self.get_objeto_info(id_objeto)
        if not objeto_info:
            return 0.0

        potencia_w = objeto_info['potencia_w']
        duracion_horas = duracion_minutos / 60
        consumo_kwh = (potencia_w * duracion_horas) / 1000
        gasto = consumo_kwh * tarifa_cop_kwh  # Multiplica por la tarifa

        return round(gasto, 2)
    
    # Función para obtener el estado actual de todos los LEDs (estado global)
    def get_current_led_states(self, id_usuario: int) -> Dict[str, int]:
        conn = self.db.conexion()
        cursor = conn.cursor()
        
        try:
            # Consulta simplificada para obtener el último estado de cada LED independientemente del usuario
            sql = """
                SELECT 
                    r1.id_objeto, 
                    r1.estado
                FROM reportes r1
                INNER JOIN (
                    SELECT 
                        id_objeto,
                        MAX(id) as max_id
                    FROM reportes
                    GROUP BY id_objeto
                ) r2 ON r1.id_objeto = r2.id_objeto AND r1.id = r2.max_id
                ORDER BY r1.id_objeto
            """
            cursor.execute(sql)
            resultados = cursor.fetchall()
            
            # Convertir los resultados a un diccionario {led_id: estado}
            estados: Dict[str, int] = {}
            for resultado in resultados:
                estado_bruto = resultado['estado']
                estado_normalizado = 1 if int(estado_bruto) == 1 else 0
                estados[str(resultado['id_objeto'])] = estado_normalizado
            
            return estados
            
        except Exception as e:
            print(f"Error al obtener estados de LEDs: {e}")
            return None
            
        finally:
            cursor.close()
            conn.close()

    def list_users(self) -> List[Dict[str, Optional[str]]]:
        conn = self.db.conexion()
        cursor = conn.cursor()
        try:
            sql = """
                SELECT u.id, u.usuario, COALESCE(r.rol, 'USER') AS rol
                FROM usuarios u
                LEFT JOIN roles_usuarios ru ON u.id = ru.id_usuario
                LEFT JOIN roles r ON ru.id_rol = r.id
                ORDER BY u.id ASC
            """
            cursor.execute(sql)
            result = cursor.fetchall()
            return result if result else []
        except Exception as error:
            raise RuntimeError(f"No se pudieron obtener los usuarios: {error}") from error
        finally:
            cursor.close()
            conn.close()

    def get_user(self, user_id: int) -> Optional[Dict[str, Optional[str]]]:
        conn = self.db.conexion()
        cursor = conn.cursor()
        try:
            sql = """
                SELECT u.id, u.usuario, u.contrasena, COALESCE(r.rol, 'USER') AS rol
                FROM usuarios u
                LEFT JOIN roles_usuarios ru ON u.id = ru.id_usuario
                LEFT JOIN roles r ON ru.id_rol = r.id
                WHERE u.id = %s
            """
            cursor.execute(sql, (user_id,))
            return cursor.fetchone()
        except Exception as error:
            raise RuntimeError(f"No se pudo obtener el usuario: {error}") from error
        finally:
            cursor.close()
            conn.close()

    def list_roles(self) -> List[str]:
        conn = self.db.conexion()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT rol FROM roles ORDER BY id ASC")
            rows = cursor.fetchall()
            return [row["rol"] for row in rows] if rows else []
        except Exception as error:
            raise RuntimeError(f"No se pudieron obtener los roles: {error}") from error
        finally:
            cursor.close()
            conn.close()

    def update_user(self, user_id: int, usuario: str, contrasena: str, rol: str) -> None:
        conn = self.db.conexion()
        cursor = conn.cursor()
        try:
            conn.begin()
            cursor.execute(
                "UPDATE usuarios SET usuario = %s, contrasena = %s WHERE id = %s",
                (usuario, contrasena, user_id),
            )
            if cursor.rowcount == 0:
                raise RuntimeError("Usuario no encontrado")
            role_id = self._get_role_id(cursor, rol)
            if role_id is None:
                raise ValueError("Rol inválido")
            cursor.execute("DELETE FROM roles_usuarios WHERE id_usuario = %s", (user_id,))
            cursor.execute(
                "INSERT INTO roles_usuarios (id_usuario, id_rol) VALUES (%s, %s)",
                (user_id, role_id),
            )
            conn.commit()
        except Exception as error:
            conn.rollback()
            raise RuntimeError(f"No se pudo actualizar el usuario: {error}") from error
        finally:
            cursor.close()
            conn.close()

    def set_user_role(self, user_id: int, rol: str) -> None:
        conn = self.db.conexion()
        cursor = conn.cursor()
        try:
            conn.begin()
            role_id = self._get_role_id(cursor, rol)
            if role_id is None:
                raise ValueError("Rol inválido")
            cursor.execute("DELETE FROM roles_usuarios WHERE id_usuario = %s", (user_id,))
            cursor.execute(
                "INSERT INTO roles_usuarios (id_usuario, id_rol) VALUES (%s, %s)",
                (user_id, role_id),
            )
            conn.commit()
        except Exception as error:
            conn.rollback()
            raise RuntimeError(f"No se pudo asignar el rol: {error}") from error
        finally:
            cursor.close()
            conn.close()

    def delete_user(self, user_id: int) -> None:
        conn = self.db.conexion()
        cursor = conn.cursor()
        try:
            conn.begin()
            cursor.execute("DELETE FROM reportes WHERE id_usuario = %s", (user_id,))
            cursor.execute("DELETE FROM roles_usuarios WHERE id_usuario = %s", (user_id,))
            cursor.execute("DELETE FROM usuarios WHERE id = %s", (user_id,))
            if cursor.rowcount == 0:
                raise RuntimeError("Usuario no encontrado")
            conn.commit()
        except Exception as error:
            conn.rollback()
            raise RuntimeError(f"No se pudo eliminar el usuario: {error}") from error
        finally:
            cursor.close()
            conn.close()

    def _get_role_id(self, cursor, rol: str) -> Optional[int]:
        cursor.execute("SELECT id FROM roles WHERE rol = %s", (rol,))
        row = cursor.fetchone()
        if not row:
            return None
        return int(row["id"])
