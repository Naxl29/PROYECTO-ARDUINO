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

        if led_id == "ALL":
            objetos = self.model.get_all_objetos()
            for obj in objetos:
                id_objeto = obj["id"]  # id de cada objeto en la tabla "objetos"
                self._procesar_estado_led(id_usuario, estado, id_objeto)
            return True
        else:
            id_objeto = int(led_id)
            return self._procesar_estado_led(id_usuario, estado, id_objeto)

    def _procesar_estado_led(self, id_usuario, estado, id_objeto):
        objeto_info = self.model.get_objeto_info(id_objeto)

        if not objeto_info:
            duracion = 0.0
            gasto = 0.0
        else:
            potencia_w = objeto_info["potencia_w"]
            consumo_wh = objeto_info["consumo_wh"]

            if estado == "1":  # Objeto encendido
                duracion = 0.0
                gasto = 0.0
            else:  # Objeto apagado
                duracion_real = self.model.calcular_duracion(id_usuario, id_objeto)
                duracion = duracion_real if duracion_real else 0.0
                gasto = consumo_wh * (duracion / 60.0) if duracion > 0 else 0.0

        return self.model.create_blo(id_usuario, id_objeto, duracion, estado, gasto)
    
    #Función para iniciar sesión
    def login(self, usuario, contrasena):
        user = self.model.login(usuario, contrasena)
        if user:
            return user 
        return None
    
    #Función para validar que no se puedan crear dos usuarios iguales
    def usuario_existente(self, usuario):
        return self.model.usuario_existe(usuario)

