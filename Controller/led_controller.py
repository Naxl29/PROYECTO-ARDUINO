# controllers/led_controller.py
import logging
from config.arduino_service import ArduinoService

class LedController:
    def __init__(self):
        self.arduino = ArduinoService()

    def manejar_estado(self, estado, led_id):
        """
        Cambia el estado de un LED específico o todos en el Arduino por WiFi.
        estado: '1' (encender), '0' (apagar)
        led_id: '1'...'8' o 'ALL'
        """
        try:
            if led_id not in ['1','2','3','4','5','6','7','8', '9','ALL']:
                return False

            ok = self.arduino.send_command(estado, led_id)

            if ok:
                logging.info(f"LED {led_id} → estado {estado}")
            else:
                logging.warning(f"Error al cambiar estado de LED {led_id} → {estado}")

            return ok
        except Exception as e:
            logging.error(f"Error en manejar_estado: {str(e)}")
            return False
