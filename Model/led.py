import serial
import time
from config import Config # Importamos el archivo de configuración

class Led:
    def __init__(self, timeout=1):
        self.puerto = Config.ARDUINO_PORT
        self.baudrate = Config.ARDUINO_BAUDRATE
        self.timeout = timeout
        try:
            self.serial = serial.Serial(self.puerto, self.baudrate, timeout=self.timeout)
            time.sleep(2)  # Espera a que Arduino resetee y esté listo
        except serial.SerialException as e:
            print(f"Error abriendo puerto serial: {e}")
            self.serial = None

    def encender(self):
        if self.serial and self.serial.is_open:
            self.serial.write(b'1')  # Envía '1' para encender led en Arduino
            print("Comando para encender LED enviado")
        else:
            print("Puerto serial no está abierto")

    def apagar(self):
        if self.serial and self.serial.is_open:
            self.serial.write(b'0')  # Envía '0' para apagar led en Arduino
            print("Comando para apagar LED enviado")
        else:
            print("Puerto serial no está abierto")

    def cerrar(self):
        if self.serial and self.serial.is_open:
            self.serial.close()
            print("Puerto serial cerrado")
