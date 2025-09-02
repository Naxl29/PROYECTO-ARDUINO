#Conexión con la base de datos
import mysql.connector
from mysql.connector import Error
from config.config import Config

class Database:
    def __init__(self):
        self.host = Config.DB_HOST
        self.database = Config.DB_DATABASE
        self.user = Config.DB_USER
        self.password = Config.DB_PASSWORD
        
    def conexion(self):
        try:
            conn = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            return conn
        except Error as e:
            return str(e)
