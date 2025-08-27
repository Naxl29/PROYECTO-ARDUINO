# Controller para los LEDs del Arduino
import serial
import time
import logging
from config import Config # Importamos el archivo de configuración

class LedController:

    def __init__(self):
        self.puerto_serial = Config.ARDUINO_PORT # Puerto serial del Arduino
        self.baudrate = Config.ARDUINO_BAUDRATE # Baudrate para la comunicación
        self.arduino = None
        self.conectado = False
        self.conectar()

    def conectar(self):
        try:
            self.arduino = serial.Serial(self.puerto_serial, self.baudrate, timeout=1)
            time.sleep(2)
            self.conectado = True
            logging.info(f"Conectado a Arduino en {self.puerto_serial}")
            return True
        except Exception as e:
            logging.error(f"Error al conectar con Arduino: {str(e)}")
            self.conectado = False
            return False

    def enviar_comando(self, comando):
        if not self.conectado:
            if not self.conectar():
                return "Arduino no conectado"

        try:
            self.arduino.write(f"{comando}\n".encode())
            time.sleep(0.1)
            respuesta = self.arduino.readline().decode().strip()
            return respuesta
        except Exception as e:
            logging.error(f"Error al enviar comando a Arduino: {str(e)}")
            self.conectado = False
            return f"Error: {str(e)}"

    def manejar_estado(self, estado, led_id):
        """
        Cambia el estado de un LED específico o todos.
        estado: '1' (encender), '0' (apagar)
        led_id: '1', '2', '3', '4' o 'ALL'
        """
        try:
            if led_id not in ['1', '2', '3', '4', 'ALL']:
                return False

            comando = f"ON{led_id}" if estado == "1" else f"OFF{led_id}"
            respuesta = self.enviar_comando(comando)

            if any(x in respuesta for x in ["encendido", "apagado"]):
                logging.info(f"LED {led_id} → estado {estado} ({respuesta})")
                return True
            else:
                logging.warning(f"Respuesta inesperada: {respuesta}")
                return False
        except Exception as e:
            logging.error(f"Error al manejar estado del LED: {str(e)}")
            return False
