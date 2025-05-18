#Controller para el usuario, en el cual se maneja cuando se registra un nuevo usuario y cuando se enciende o se apaga el botón
from Model.bloque import Bloque
from flask import session, redirect, url_for

class BloqueController:
    def __init__(self):
        self.model = Bloque()
    
    #Función para guardar un nuevo usuario
    def save(self, usuario, contrasena):
        id = self.model.create_user(usuario, contrasena)
        return id
    
    #Función para guardar el estado del botón (encendido o apagado)
    def save_estado(self, id_usuario, estado):
        id_usuario = int(id_usuario)
        resultado = self.model.create_blo(id_usuario, estado)
        return resultado
    
    #Función para iniciar sesión
    def login(self, usuario, contrasena):
        user = self.model.login(usuario, contrasena)
        if user:
            return user 
        return None
    
    #Función para validar que no se puedan crear dos usuarios iguales
    def usuario_existente(self, usuario):
        return self.model.usuario_existe(usuario)

