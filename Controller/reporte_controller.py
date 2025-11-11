#Controller para manejar el blockchain, en el cual se muestra el historial y los hashes
from Model.reporte import Reporte

class ReporteController:
    def __init__(self):
        self.model = Reporte()

    #Muestra los detalles del usuario cuando se crea
    def show(self, id):
        return self.model.show(id)
    
    #Muestra el reporte
    def see(self, id_usuario=None, user_role=None):
        bloques = self.model.see(id_usuario, user_role)
        total_gasto = sum(b['gasto'] for b in bloques) if bloques else 0
        return bloques, total_gasto
    
    #Esta función queda inactiva para la nueva actualización del proyecto
    #Función para mostrar el historial de los hashes (hash anterior y hash actual)
    def get_block_by_hash(self, block_hash):
        conn = self.model.db.conexion() 
        cursor = conn.cursor()

        sql = "SELECT * FROM blockchain WHERE hash = %s LIMIT 1"
        cursor.execute(sql, (block_hash,))
        block = cursor.fetchone()

        cursor.close()
        conn.close()

        return block