# Modelo simple para datos de energía
from Model.database import Database

class EnergiaModel:
    
    def __init__(self):
        self.db = Database()
    
    def obtener_consumo(self):
        """Obtiene el promedio de gasto en COP de TODOS los reportes"""
        try:
            conn = self.db.conexion()
            cursor = conn.cursor()
            cursor.execute("SELECT AVG(gasto) as promedio FROM reportes WHERE gasto > 0")
            resultado = cursor.fetchone()
            cursor.close()
            conn.close()
            return float(resultado['promedio']) if resultado and resultado['promedio'] else 50.0
        except:
            return 50.0
    
    def obtener_gasto_mes(self):
        """Obtiene el gasto total del mes actual"""
        try:
            conn = self.db.conexion()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT SUM(gasto) as gasto_mes 
                FROM reportes 
                WHERE MONTH(fecha) = MONTH(CURDATE()) 
                AND YEAR(fecha) = YEAR(CURDATE())
                AND gasto > 0
            """)
            resultado = cursor.fetchone()
            cursor.close()
            conn.close()
            return float(resultado['gasto_mes']) if resultado and resultado['gasto_mes'] else 0.0
        except:
            return 0.0
    
    def obtener_datos(self):
        """Obtiene datos básicos de reportes con fecha y gasto"""
        try:
            conn = self.db.conexion()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    MONTH(fecha) as mes,
                    SUM(gasto) as gasto_total
                FROM reportes 
                WHERE gasto > 0 
                GROUP BY MONTH(fecha)
                ORDER BY fecha
            """)
            datos = cursor.fetchall()
            cursor.close()
            conn.close()
            return datos
        except:
            return []  # Retorna una lista vacía en caso de error
