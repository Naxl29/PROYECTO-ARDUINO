#Conexión con la base de datos
import pymysql
from config.config import Config

class Database:
    def __init__(self):
        self.host = Config.DB_HOST
        self.port = Config.DB_PORT
        self.database = Config.DB_DATABASE
        self.user = Config.DB_USER
        self.password = Config.DB_PASSWORD
        
    def conexion(self):
        try:
            conn = pymysql.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port,
                connect_timeout=10,
                charset='utf8mb4',
                autocommit=True,
                # Configuración específica para Railway
                cursorclass=pymysql.cursors.DictCursor
            )
            print(f"✅ Conexión exitosa a MySQL - Host: {self.host}")
            return conn
        except Exception as e:
            print(f"ERROR de MySQL: {e}")
            print(f"Host: {self.host}")
            print(f"Database: {self.database}")
            print(f"User: {self.user}")
            raise Exception(f"Error de conexión a la base de datos: {e}")
