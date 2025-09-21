import requests
from config.config import Config 

class Led:
    def __init__(self):
        self.base_url = Config.BASE_URL

    def encender(self, led_id):
        try:
            url = f"{self.base_url}/ON{led_id}"
            r = requests.get(url, timeout=3)
            return r.status_code == 200
        except Exception as e:
            print(f"Error al encender LED {led_id}: {e}")
            return False

    def apagar(self, led_id):
        try:
            url = f"{self.base_url}/OFF{led_id}"
            r = requests.get(url, timeout=3)
            return r.status_code == 200
        except Exception as e:
            print(f"Error al apagar LED {led_id}: {e}")
            return False
        
