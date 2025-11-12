from __future__ import annotations

from threading import Lock
from typing import Optional

from simple_websocket import ConnectionClosed, Server


class ArduinoConnectionNotAvailable(RuntimeError):
    pass


_connection_lock = Lock()
_active_connection: Optional[Server] = None


def set_connection(connection: Server) -> None:
    if connection is None:
        raise ValueError("connection no puede ser None")
    global _active_connection
    with _connection_lock:
        _active_connection = connection


def clear_connection(connection: Optional[Server]) -> None:
    global _active_connection
    with _connection_lock:
        if connection is None or connection is _active_connection:
            _active_connection = None


def has_connection() -> bool:
    with _connection_lock:
        return _active_connection is not None


def send_text(message: str) -> None:
    if not message:
        raise ValueError("message no puede ser vacío")
    with _connection_lock:
        connection = _active_connection
    if connection is None:
        raise ArduinoConnectionNotAvailable("No hay conexión WebSocket activa con el Arduino.")
    try:
        connection.send(message)
    except ConnectionClosed as error:
        clear_connection(connection)
        raise ArduinoConnectionNotAvailable("La conexión WebSocket con el Arduino se cerró.") from error

