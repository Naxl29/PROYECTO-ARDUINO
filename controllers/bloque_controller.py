from models.bloque import Bloque
from flask import session, redirect, url_for

class BloqueController:
    def __init__(self):
        self.model = Bloque()
    
    def save(self, usuario, contrasena):
        id = self.model.create_user(usuario, contrasena)
        return id
    
    def save_estado(self, id_usuario, estado):
        id_usuario = int(id_usuario)
        resultado = self.model.create_blo(id_usuario, estado)
        return resultado
    
    def login(self, usuario, contrasena):
        user = self.model.login(usuario, contrasena)
        if user:
            session['usuario'] = user['usuario']
            session['id_usuario'] = user['id']
            return True
        return False
