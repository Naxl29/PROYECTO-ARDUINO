from datetime import datetime
from Model.database import Database

class Reporte:
    def __init__(self):
        self.db = Database()

    #Muestra los reportes de historial al encender cada botón
    def see(self):
        conn = self.db.conexion()
        cursor = conn.cursor(dictionary=True)

        sql = """
            SELECT r.id, 
            r.id_usuario, 
            o.objeto, 
            o.potencia_w, 
            o.consumo_wh, 
            r.fecha, 
            r.duracion_minutos, 
            r.estado, 
            r.gasto
            FROM reportes r
            JOIN objetos o ON r.id_objeto = o.id
            ORDER BY r.id DESC 
            """
        cursor.execute(sql)

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
    