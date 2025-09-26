import json
import os
from typing import Dict


ALLOWED_LED_IDS = [str(i) for i in range(1, 9)]  # '1'..'8'


def _store_path() -> str:
    """Return absolute path to the JSON store for LED names."""
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    data_dir = os.path.join(base_dir, 'data')
    os.makedirs(data_dir, exist_ok=True)
    return os.path.join(data_dir, 'leds.json')


def _load_store() -> Dict:
    path = _store_path()
    if not os.path.exists(path):
        return {"led_names": {}}
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if not isinstance(data, dict):
                return {"led_names": {}}
            data.setdefault("led_names", {})
            return data
    except Exception:
        # Corrupt or unreadable file: start fresh
        return {"led_names": {}}


def _save_store(data: Dict) -> None:
    path = _store_path()
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_led_names(base_led_names: Dict[str, str]) -> Dict[str, str]:
    """
    Merge persisted custom names over the provided base names.
    Never adds new IDs outside 1..8; 'ALL' is kept from base.
    """
    data = _load_store()
    overrides = data.get("led_names", {})
    merged = dict(base_led_names)
    for led_id, name in overrides.items():
        if led_id in ALLOWED_LED_IDS and isinstance(name, str) and name.strip():
            merged[led_id] = name.strip()
    return merged


def save_led_name(led_id: str, name: str) -> bool:
    """Persist a custom human-friendly name for a given LED id (1..8)."""
    if led_id not in ALLOWED_LED_IDS:
        return False
    if not isinstance(name, str) or not name.strip():
        return False
    # Normalizar a MAYÚSCULAS y acotar longitud
    name = name.strip().upper()
    if len(name) > 60:
        name = name[:60]
    data = _load_store()
    data.setdefault("led_names", {})
    data["led_names"][led_id] = name.strip()
    _save_store(data)
    return True
