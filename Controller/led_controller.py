import logging
from config.arduino_connection import ArduinoConnectionNotAvailable
from config.arduino_service import ArduinoService


class LedController:
    def __init__(self):
        self.arduino = ArduinoService()

    def manejar_estado(self, estado: str, led_id: str) -> None:
        if led_id not in {'1', '2', '3', '4', '5', '6', '7', '8', '9', 'ALL'}:
            raise ValueError("Identificador de LED inválido.")
        try:
            self.arduino.send_command(estado, led_id)
            logging.info("LED %s → estado %s", led_id, estado)
        except ArduinoConnectionNotAvailable:
            logging.error("No hay conexión WebSocket activa con el Arduino.")
            raise
        except ValueError as error:
            logging.error("Error de validación al enviar comando: %s", error)
            raise
