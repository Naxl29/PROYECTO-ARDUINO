#Conexión con la base de datos
import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self):
        self.host = "localhost"
        self.database = "blockchain"
        self.user = "root"
        self.password = ""
        
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
