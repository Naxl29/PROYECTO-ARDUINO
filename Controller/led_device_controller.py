from typing import List, Dict
from Model.led_device import LedDeviceModel
from Model.database import Database
from config.roles_config import LED_NAMES
from utils.leds_store import get_led_names
from config.arduino_service import ArduinoService


class LedDeviceController:
    def __init__(self):
        self.arduino = ArduinoService()

    def list_devices(self) -> List[Dict]:
        return LedDeviceModel.list_leds()

    def create_device(self, nombre: str, potencia: float, consumo: float, color: str) -> int:
        # Choose next available channel automatically
        channel = LedDeviceModel.next_channel()
        # Normalizar a MAYÚSCULAS por consistencia visual y de búsqueda
        nombre_up = (nombre or '').strip().upper()
        # Creamos el dispositivo; ignoramos el ID autoincremental y devolvemos el canal asignado
        LedDeviceModel.create(channel, nombre_up, potencia, consumo, color)
        return channel

    def list_base_leds(self) -> List[Dict]:
        """Return the 8 static LEDs with enriched metadata: name overrides and objeto pot/cons if available."""
        # Colors for 1..8 consistent with button.css comments
        default_colors = {
            '1': '#ff4444', '2': '#44ff44', '3': '#4444ff', '4': '#ffff44',
            '5': '#ff44ff', '6': '#44ffff', '7': '#ff8c00', '8': '#8a2be2'
        }
        # Get friendly names (overrides JSON over defaults from roles_config)
        friendly_names = get_led_names(LED_NAMES)
        # Try to read potencia/consumo from objetos table
        pot_map = {}
        try:
            conn = Database().conexion()
            with conn.cursor() as cur:
                cur.execute("SELECT id, potencia_w, consumo_wh, objeto FROM objetos WHERE id BETWEEN 1 AND 8")
                for row in cur.fetchall() or []:
                    pot_map[str(row['id'])] = {
                        'potencia': row.get('potencia_w', 0) or 0,
                        'consumo': row.get('consumo_wh', 0) or 0,
                        'objeto': row.get('objeto')
                    }
            conn.close()
        except Exception:
            # If objetos table doesn't exist or error occurs, fall back to zeros
            pot_map = {}

        result = []
        for i in range(1, 9):
            key = str(i)
            meta = pot_map.get(key, {})
            nombre = friendly_names.get(key, f'LED {i}')
            # Prefer objeto field if present and non-empty
            if meta.get('objeto'):
                nombre = meta['objeto']
            result.append({
                'channel': key,
                'nombre': nombre,
                'potencia': meta.get('potencia', 0),
                'consumo': meta.get('consumo', 0),
                'color': default_colors.get(key, '#ffffff')
            })
        return result

    def send_state(self, channel: str, estado: str) -> bool:
        # Delegate to ArduinoService directly (channel maps to led_id)
        try:
            return self.arduino.send_command(estado, channel)
        except Exception:
            return False
