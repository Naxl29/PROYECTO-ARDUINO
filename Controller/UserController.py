from Models import User
class UserController:
    def __init__(self, db_connection):
         
        self.model = User(self)  # Modelo de usuarios

    def createUser(self, usuario, contrasena):
        # Crear un nuevo usuario
        return self.model.createUser(usuario, contrasena)

    def login(self, usuario, contrasena):
        # Iniciar sesión de un usuario
        return self.model.login(usuario, contrasena)

    def show_user(self, id):
        # Mostrar información de un usuario
        return self.model.show(id)  
    
