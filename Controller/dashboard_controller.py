from Model.database import Database

class DashboardController:
    def __init__(self):
        self.db = Database()
    
    def get_dashboard_stats(self, user_role):
        """
        Obtiene todas las estadísticas necesarias para el dashboard
        """
        conn = self.db.conexion()
        cursor = conn.cursor(dictionary=True)
        
        try:
            # Total de usuarios
            cursor.execute("SELECT COUNT(*) AS total_usuarios FROM usuarios")
            total_usuarios = cursor.fetchone()['total_usuarios']

            # Total de LEDs encendidos
            cursor.execute("SELECT COUNT(*) AS total_encendidos FROM reportes WHERE estado = 1")
            total_encendidos = cursor.fetchone()['total_encendidos']

            # Últimos 5 encendidos
            cursor.execute("""
                SELECT u.usuario, b.fecha
                FROM reportes b
                JOIN usuarios u on b.id_usuario = u.id
                WHERE b.estado = 1
                ORDER BY b.fecha DESC
                LIMIT 5
            """)
            ultimos_encendidos = cursor.fetchall()

            # Datos para el gráfico
            cursor.execute("""
                SELECT DATE(fecha) as fecha, COUNT(*) as cantidad
                FROM reportes
                WHERE estado = 1
                GROUP BY fecha
                ORDER BY fecha ASC
            """)
            grafico_data = cursor.fetchall()
            
            return {
                'total_usuarios': total_usuarios,
                'total_encendidos': total_encendidos,
                'ultimos_encendidos': ultimos_encendidos,
                'grafico_data': grafico_data,
                'user_role': user_role
            }
            
        except Exception as e:
            print(f"Error al obtener estadísticas del dashboard: {e}")
            return None
            
        finally:
            cursor.close()
            conn.close()
