from config.conexion import mysql # de la carpeta config el archivo conexion y importamos la varible mysql 

class User:
    def __init__(self): # El contructor en python
        self.conn = None

    # Función sirve para utilizar la variable mysql en todas las funciones de este modelo
    def conectar(self): 
        self.conn = mysql.connect()
        return self.conn.cursor() # Retornamos la conexion para utilizarla despues

    # Función para crear un nuevo usuario
    def createUser(self, usuario, contrasena):
        cursor = self.conectar() # Utilizamos la funcion conectar(), para usar la conexion
        sql = "INSERT INTO usuarios (usuario, contrasena) VALUES (%s, %s)"
        cursor.execute(sql, (usuario, contrasena))
        self.conn.commit()
        id_usuario = cursor.lastrowid # Esta varible nos dara el id del usuario que se acabo de crear 
        self.conn.close()
        return id_usuario # Retornamos el id del usuario para usarlo en la funcion createBlock

    # función para iniciar sesión en la pagina 
    def login(self, usuario, contrasena):
        conn = self.conectar() # conexion
        cursor = conn.cursor(dictionary=True) # Nos traera la informacion en forma de diccionario
        sql = "SELECT * FROM usuarios WHERE usuario = %s AND contrasena = %s"
        cursor.execute(sql, (usuario, contrasena))
        fila = cursor.fetchone() # Esta variable nos extrea la informacion del usuario de la base de datos en forma de fila que intenta iniciar sesión 
        conn.close()
        return fila if fila else False # Si hay el la información coicide los traera la fila, si no nos retorna false
    
    # Función para mostrar la información del usuario que se acaa de crear 
    def show(self, id):
        conn = self.conectar() # Se utiliza la conexion
        cursor = conn.cursor(dictionary=True) 
        sql = "SELECT * FROM usuarios WHERE id = %s LIMIT 1"
        cursor.execute(sql, (id,))
        fila = cursor.fetchone() # Nos muestra la información del usuario acabado de crear
        conn.close()
        return fila if fila else False # Si hay el la información coicide los traera la fila, si no nos retorna false
