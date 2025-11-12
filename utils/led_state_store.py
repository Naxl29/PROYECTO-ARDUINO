from __future__ import annotations

import json
import os
from datetime import datetime
from typing import Dict, Mapping, Optional, TypedDict, Literal


LedState = Literal["0", "1"]
LedStates = Dict[str, LedState]


class _PersistedStates(TypedDict, total=False):
    led_states: Dict[str, LedState]
    updated_at: str


def _store_path() -> str:
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    data_dir = os.path.join(base_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    return os.path.join(data_dir, "led_states.json")


def _normalize_state(value: object) -> Optional[LedState]:
    if isinstance(value, str):
        stripped = value.strip()
        if stripped == "1":
            return "1"
        if stripped == "0":
            return "0"
    if isinstance(value, bool):
        return "1" if value else "0"
    if isinstance(value, int):
        return "1" if value == 1 else "0" if value == 0 else None
    return None


def _load_raw() -> _PersistedStates:
    path = _store_path()
    if not os.path.exists(path):
        return _PersistedStates(led_states={}, updated_at=datetime.utcnow().isoformat())
    try:
        with open(path, "r", encoding="utf-8") as handle:
            payload = json.load(handle)
            if not isinstance(payload, dict):
                return _PersistedStates(led_states={})
            led_states = payload.get("led_states")
            if isinstance(led_states, dict):
                cleaned: Dict[str, LedState] = {}
                for raw_key, raw_value in led_states.items():
                    key = str(raw_key)
                    normalized = _normalize_state(raw_value)
                    if normalized is not None:
                        cleaned[key] = normalized
                return _PersistedStates(
                    led_states=cleaned,
                    updated_at=str(payload.get("updated_at", "")),
                )
            return _PersistedStates(led_states={})
    except (OSError, json.JSONDecodeError):
        return _PersistedStates(led_states={})


def read_states() -> LedStates:
    payload = _load_raw()
    led_states = payload.get("led_states", {})
    return dict(led_states)


def persist_states(states: Mapping[str, LedState]) -> None:
    filtered: Dict[str, LedState] = {}
    for key, value in states.items():
        normalized = _normalize_state(value)
        if normalized is not None:
            filtered[str(key)] = normalized
    payload: _PersistedStates = _PersistedStates(
        led_states=filtered,
        updated_at=datetime.utcnow().isoformat(),
    )
    path = _store_path()
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=True, indent=2)


def write_state(led_id: str, estado: LedState) -> LedStates:
    states = read_states()
    states[str(led_id)] = estado
    persist_states(states)
    return states


def merge_states(primary: Mapping[str, LedState], fallback: Mapping[str, LedState]) -> LedStates:
    merged: LedStates = {}
    for key, value in fallback.items():
        normalized = _normalize_state(value)
        if normalized is not None:
            merged[str(key)] = normalized
    for key, value in primary.items():
        normalized = _normalize_state(value)
        if normalized is not None:
            merged[str(key)] = normalized
    return merged

