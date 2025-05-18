#Controller para la luz led del arduino
import serial
import time
import logging

class LedController:
    def __init__(self, pin=13, puerto_serial='COM3', baudrate=9600):

        """
        Inicializa el controlador del LED
        
        Args:
            pin (int): Número de pin donde está conectado el LED en Arduino
            puerto_serial (str): Puerto serial donde está conectado Arduino
            baudrate (int): Velocidad de comunicación con Arduino
        """
        self.pin = pin
        self.puerto_serial = puerto_serial
        self.baudrate = baudrate
        self.arduino = None
        self.conectado = False
        
        self.conectar()
    
    def conectar(self):
        """Establece conexión con Arduino"""
        try:
            self.arduino = serial.Serial(self.puerto_serial, self.baudrate, timeout=1)
            time.sleep(2)  # Esperar a que Arduino se reinicie
            self.conectado = True
            logging.info(f"Conectado a Arduino en {self.puerto_serial}")
            return True
        except Exception as e:
            logging.error(f"Error al conectar con Arduino: {str(e)}")
            self.conectado = False
            return False
    
    def enviar_comando(self, comando):
        """
        Envía un comando a Arduino
        
        Args:
            comando (str): Comando a enviar ('ON' o 'OFF')
            
        Returns:
            str: Respuesta de Arduino o mensaje de error
        """
        if not self.conectado:
            if not self.conectar():
                return "Arduino no conectado"
        
        try:
            # Enviar comando a Arduino
            self.arduino.write(f"{comando}\n".encode())
            time.sleep(0.1)
            
            # Leer respuesta de Arduino
            respuesta = self.arduino.readline().decode().strip()
            return respuesta
        except Exception as e:
            logging.error(f"Error al enviar comando a Arduino: {str(e)}")
            self.conectado = False
            return f"Error: {str(e)}"
    
    def manejar_estado(self, estado):
        """
        Maneja el estado del LED
        
        Args:
            estado (str): Estado del LED ('0' para apagado, '1' para encendido)
            
        Returns:
            bool: True si se pudo cambiar el estado, False en caso contrario
        """
        try:
            # Convertir estado a comando para Arduino
            comando = "ON" if estado == "1" else "OFF"
            
            # Enviar comando a Arduino
            respuesta = self.enviar_comando(comando)
            
            # Verificar respuesta
            if "LED encendido" in respuesta or "LED apagado" in respuesta:
                logging.info(f"LED cambiado a estado {estado}: {respuesta}")
                return True
            else:
                logging.warning(f"Respuesta inesperada de Arduino: {respuesta}")
                return False
        except Exception as e:
            logging.error(f"Error al manejar estado del LED: {str(e)}")
            return False