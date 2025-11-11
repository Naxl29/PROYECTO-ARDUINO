from typing import List, Dict, Optional
from Model.database import Database


class LedDeviceModel:

    @staticmethod
    def list_leds() -> List[Dict]:
        conn = Database().conexion()
        with conn.cursor() as cur:
            try:
                cur.execute(
                    "SELECT id AS channel, objeto AS nombre, potencia_w AS potencia, consumo_wh AS consumo, color FROM objetos WHERE id > 9 ORDER BY id ASC"
                )
                rows = cur.fetchall() or []
            except Exception:
                rows = []
        conn.close()
        # Normalizar salida para mantener interfaz anterior (channel como str)
        for r in rows:
            r['channel'] = str(r['channel'])
            if not r.get('color'):
                r['color'] = '#ffffff'
        return rows

    @staticmethod
    def list_channels() -> List[str]:
        return [row['channel'] for row in LedDeviceModel.list_leds()]

    @staticmethod
    def next_channel() -> str:
        conn = Database().conexion()
        with conn.cursor() as cur:
            try:
                cur.execute("SELECT MAX(id) AS max_id FROM objetos")
                row = cur.fetchone()
                max_id = row.get('max_id') or 9
            except Exception:
                max_id = 9
        conn.close()
        if max_id < 9:
            max_id = 9
        return str(int(max_id) + 1)

    @staticmethod
    def get_by_channel(channel: str) -> Optional[Dict]:
        if not str(channel).isdigit():
            return None
        conn = Database().conexion()
        with conn.cursor() as cur:
            try:
                cur.execute(
                    "SELECT id AS channel, objeto AS nombre, potencia_w AS potencia, consumo_wh AS consumo, color FROM objetos WHERE id=%s",
                    (int(channel),)
                )
                row = cur.fetchone()
            except Exception:
                row = None
        conn.close()
        if row:
            row['channel'] = str(row['channel'])
            if not row.get('color'):
                row['color'] = '#ffffff'
        return row

    @staticmethod
    def update(channel: str, nombre: str, potencia: float, consumo: float, color: str) -> None:
        if not str(channel).isdigit():
            return
        conn = Database().conexion()
        with conn.cursor() as cur:
            try:
                nombre_up = (nombre or '').strip().upper()
            except Exception:
                nombre_up = str(nombre).upper() if nombre is not None else ''
            # Asegurar fila existente (upsert)
            cur.execute(
                """
                INSERT INTO objetos (id, objeto, potencia_w, consumo_wh, color)
                VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE objeto=VALUES(objeto), potencia_w=VALUES(potencia_w),
                    consumo_wh=VALUES(consumo_wh), color=VALUES(color)
                """,
                (int(channel), nombre_up, potencia, consumo, color or '#ffffff')
            )
        conn.commit()
        conn.close()

    @staticmethod
    def create(channel: str, nombre: str, potencia: float, consumo: float, color: str) -> int:
        if not str(channel).isdigit():
            return -1
        conn = Database().conexion()
        with conn.cursor() as cur:
            try:
                nombre_up = (nombre or '').strip().upper()
            except Exception:
                nombre_up = str(nombre).upper() if nombre is not None else ''
            cur.execute(
                """
                INSERT INTO objetos (id, objeto, potencia_w, consumo_wh, color)
                VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE objeto=VALUES(objeto), potencia_w=VALUES(potencia_w),
                    consumo_wh=VALUES(consumo_wh), color=VALUES(color)
                """,
                (int(channel), nombre_up, potencia, consumo, color or '#ffffff')
            )
        conn.commit()
        conn.close()
        return int(channel)

    @staticmethod
    def delete(channel: str) -> None:
        if not str(channel).isdigit():
            return
        conn = Database().conexion()
        with conn.cursor() as cur:
            # Eliminar de objetos
            try:
                cur.execute("DELETE FROM objetos WHERE id=%s", (int(channel),))
            except Exception:
                pass
            # Limpieza auxiliar (asignaciones y flags)
            try:
                cur.execute("DELETE FROM dispositivo_secciones WHERE channel=%s", (str(channel),))
            except Exception:
                try:
                    cur.execute("DELETE FROM device_sections WHERE channel=%s", (str(channel),))
                except Exception:
                    pass
            try:
                cur.execute("DELETE FROM device_flags WHERE channel=%s", (str(channel),))
            except Exception:
                pass
        conn.commit()
        conn.close()
