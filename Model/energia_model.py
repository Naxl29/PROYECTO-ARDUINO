# Modelo simple para datos de energía
from Model.database import Database

class EnergiaModel:
    
    def __init__(self):
        self.db = Database()
    
    def obtener_consumo(self):
        """Obtiene el promedio de gasto de los últimos reportes"""
        try:
            conn = self.db.conexion()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT AVG(gasto) as promedio FROM reportes ORDER BY fecha DESC LIMIT 3")
            resultado = cursor.fetchone()
            cursor.close()
            conn.close()
            return float(resultado['promedio']) if resultado and resultado['promedio'] else 0.5
        except:
            return 0.5
    
    def obtener_datos(self):
        """Obtiene datos reales de reportes para entrenar """
        try:
            conn = self.db.conexion()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT gasto as consumo_kwh, (gasto * 2500) as costo FROM reportes WHERE gasto > 0")
            datos = cursor.fetchall()
            cursor.close()
            conn.close()
            return datos
        except:
            return []  # Retorna una lista vacía en caso de error
