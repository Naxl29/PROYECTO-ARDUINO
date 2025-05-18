import serial
import time

class Led:
    def __init__(self, puerto='COM3', baudrate=9600, timeout=1):
        self.puerto = puerto
        self.baudrate = baudrate
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
