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
        
        # Obtener información del objeto desde la base de datos
        objeto_info = self.model.get_objeto_info(id_objeto)
        
        if not objeto_info:
            # Si no se encuentra el objeto, usar valores por defecto
            duracion = 0.0
            gasto = 0.0
        else:
            # Usar los valores reales de la base de datos
            potencia_w = objeto_info['potencia_w']
            consumo_wh = objeto_info['consumo_wh']
            
            if estado == '1':  # LED encendido
                # Al encender, solo registramos el momento de inicio
                duracion = 0.0  # Sin duración al encender
                gasto = 0.0     # Sin gasto al encender
            else:  # LED apagado
                # Al apagar, calculamos la duración real desde el último encendido
                duracion_real = self.model.calcular_duracion(id_usuario, id_objeto)
                duracion = duracion_real if duracion_real else 0.0
                
                # Calcular gasto real basado en la duración real de uso
                # consumo_wh * (duracion_minutos / 60) para convertir a horas
                gasto = consumo_wh * (duracion / 60.0) if duracion > 0 else 0.0
            
        resultado = self.model.create_blo(id_usuario, id_objeto, duracion, estado, gasto)
        return resultado
    
    #Función privada para procesar el estado del LED
    def _procesar_estado_led(self, id_usuario, estado, id_objeto):
            objeto_info = self.model.get_objeto_info(id_objeto)

            if not objeto_info:
                duracion = 0.0
                gasto = 0.0
            else:
                if estado == "1":  # Objeto encendido
                    duracion = 0.0
                    gasto = 0.0
                else:  # Objeto apagado
                    duracion_real = self.model.calcular_duracion(id_usuario, id_objeto)
                    duracion = duracion_real if duracion_real else 0.0
                    gasto = self.model.calcular_gasto(id_objeto, duracion) if duracion > 0 else 0.0

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