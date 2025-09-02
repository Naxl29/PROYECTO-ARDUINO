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
    def save_estado(self, id_usuario, estado, led_id):
        id_usuario = int(id_usuario)
        id_objeto = int(led_id)  # ID del LED como objeto
        
        # Para el registro del estado, asumimos duración mínima y gasto básico
        # Si es encendido, registramos tiempo estimado; si es apagado, tiempo 0
        if estado == '1':  # LED encendido
            duracion = 1.0  # 1 minuto como duración base
            gasto = 0.05    # Gasto estimado en unidades de energía
        else:  # LED apagado
            duracion = 0.0  # Sin duración cuando se apaga
            gasto = 0.0     # Sin gasto cuando se apaga
            
        resultado = self.model.create_blo(id_usuario, id_objeto, duracion, estado, gasto)
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

