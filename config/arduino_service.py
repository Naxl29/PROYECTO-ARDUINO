# services/arduino_service.py
import requests
import logging
from config.config import Config

class ArduinoService:
    def __init__(self):
        self.base_url = Config.BASE_URL.rstrip("/")

    def send_command(self, estado, led_id):
        """
        Envía un comando ON/OFF al Arduino por WiFi
        estado: '1' (encender) o '0' (apagar)
        led_id: '1'...'8' o 'ALL'
        """
        try:
            if led_id == "ALL":
                ok = False
                for i in range(1, 9):
                    url = f"{self.base_url}/ON{i}" if estado == "1" else f"{self.base_url}/OFF{i}"
                    logging.info(f"Enviando a Arduino: {url}")
                    try:
                        response = requests.get(url, timeout=5)
                        response.raise_for_status()
                        ok = True 
                    except Exception as e:
                        logging.warning(f"Error con LED {i}: {e}")
                        continue
                return ok

            # LED (1 a 8)
            url = f"{self.base_url}/ON{led_id}" if estado == "1" else f"{self.base_url}/OFF{led_id}"
            logging.info(f"Enviando a Arduino: {url}")
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return True

        except Exception as e:
            logging.warning(f"Error enviando a Arduino: {e}")
            return False
