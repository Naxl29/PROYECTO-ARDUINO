from datetime import datetime
from Model.database import Database

class Reporte:
    def __init__(self):
        self.db = Database()

    #Muestra los reportes de historial al encender cada botón
    def see(self, id_usuario=None, user_role='USER'):
        conn = self.db.conexion()
        cursor = conn.cursor(dictionary=True)

        if user_role == 'ADMIN':
            # Admin ve todos los reportes
            sql = """
                SELECT r.id, 
                r.id_usuario, 
                u.usuario,
                o.objeto, 
                o.potencia_w, 
                o.consumo_wh, 
                r.fecha, 
                r.duracion_minutos, 
                r.estado, 
                r.gasto
                FROM reportes r
                JOIN objetos o ON r.id_objeto = o.id
                LEFT JOIN usuarios u ON r.id_usuario = u.id
                ORDER BY r.id DESC 
                """
            cursor.execute(sql)
        else:
            # Usuario normal y niño solo ven sus propios reportes
            sql = """
                SELECT r.id, 
                r.id_usuario, 
                u.usuario,
                o.objeto, 
                o.potencia_w, 
                o.consumo_wh, 
                r.fecha, 
                r.duracion_minutos, 
                r.estado, 
                r.gasto
                FROM reportes r
                JOIN objetos o ON r.id_objeto = o.id
                LEFT JOIN usuarios u ON r.id_usuario = u.id
                WHERE r.id_usuario = %s
                ORDER BY r.id DESC 
                """
            cursor.execute(sql, (id_usuario,))

        bloques = []
        for fila in cursor.fetchall():
            fila['fecha'] = datetime.strptime(str(fila['fecha']), '%Y-%m-%d %H:%M:%S')
            bloques.append(fila)

        cursor.close()
        conn.close()

        return bloques

    #Muestra los detalles del usuario creado
    def show(self, id):
        conn = self.db.conexion()
        cursor = conn.cursor(dictionary=True)
        
        sql = "SELECT * FROM usuarios WHERE id = %s LIMIT 1"
        cursor.execute(sql, (id,))
        usuario = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return usuario
    