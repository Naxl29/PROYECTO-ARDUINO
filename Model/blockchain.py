from datetime import datetime
from Model.database import Database

class Blockchain:
    def __init__(self):
        self.db = Database()

    #Muestra el historial del botón
    def see(self):
        conn = self.db.conexion()
        cursor = conn.cursor(dictionary=True)

        sql = """
            SELECT 
                b.id, 
                b.id_usuario, 
                u.usuario, 
                b.fecha, 
                b.estado, 
                b.anterior_hash, 
                b.hash
            FROM blockchain b
            JOIN usuarios u ON b.id_usuario = u.id
            ORDER BY b.id DESC
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
    