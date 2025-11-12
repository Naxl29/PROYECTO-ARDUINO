from __future__ import annotations

import json
from typing import Dict

from config.arduino_connection import send_text


def _build_payload(estado: str, led_id: str) -> Dict[str, str]:
    if estado not in {"0", "1"}:
        raise ValueError("El estado debe ser '0' o '1'.")
    if led_id == "ALL":
        return {"type": "commandAll", "state": estado}
    if not led_id.isdigit():
        raise ValueError("El identificador del LED debe ser numérico o 'ALL'.")
    return {"type": "command", "state": estado, "led": led_id}


class ArduinoService:
    def send_command(self, estado: str, led_id: str) -> None:
        payload = _build_payload(estado, led_id)
        message = json.dumps(payload, ensure_ascii=False)
        send_text(message)
