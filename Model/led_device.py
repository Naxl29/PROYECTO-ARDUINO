from typing import List, Dict, Optional
from Model.database import Database


class LedDeviceModel:
    TABLE_SQL = (
        """
        CREATE TABLE IF NOT EXISTS leds (
            id INT AUTO_INCREMENT PRIMARY KEY,
            channel VARCHAR(10) NOT NULL UNIQUE,
            nombre VARCHAR(100) NOT NULL,
            potencia DECIMAL(10,2) DEFAULT 0,
            consumo DECIMAL(10,2) DEFAULT 0,
            color VARCHAR(7) DEFAULT '#ffffff',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
    )

    @staticmethod
    def _ensure_table(conn) -> None:
        with conn.cursor() as cur:
            cur.execute(LedDeviceModel.TABLE_SQL)

    @staticmethod
    def list_leds() -> List[Dict]:
        conn = Database().conexion()
        LedDeviceModel._ensure_table(conn)
        with conn.cursor() as cur:
            cur.execute("SELECT id, channel, nombre, potencia, consumo, color FROM leds ORDER BY id ASC")
            rows = cur.fetchall()
        conn.close()
        return rows or []

    @staticmethod
    def list_channels() -> List[str]:
        return [row['channel'] for row in LedDeviceModel.list_leds()]

    @staticmethod
    def next_channel() -> str:
        """Return next available numeric channel as string, starting after 8.
        It considers all existing numeric channels in table `leds` and returns max(8, existing)+1.
        """
        # Default baseline is 8 (the static ones), so next is 9 when no dynamic exists
        try:
            channels = LedDeviceModel.list_channels()
            max_found = 8
            for ch in channels:
                if isinstance(ch, (int, float)):
                    try:
                        ch_int = int(ch)
                    except Exception:
                        continue
                else:
                    ch_str = str(ch)
                    if ch_str.isdigit():
                        ch_int = int(ch_str)
                    else:
                        continue
                if ch_int > max_found:
                    max_found = ch_int
            return str(max_found + 1)
        except Exception:
            return "9"

    @staticmethod
    def get_by_channel(channel: str) -> Optional[Dict]:
        conn = Database().conexion()
        LedDeviceModel._ensure_table(conn)
        with conn.cursor() as cur:
            cur.execute("SELECT id, channel, nombre, potencia, consumo, color FROM leds WHERE channel=%s", (channel,))
            row = cur.fetchone()
        conn.close()
        return row

    @staticmethod
    def create(channel: str, nombre: str, potencia: float, consumo: float, color: str) -> int:
        conn = Database().conexion()
        LedDeviceModel._ensure_table(conn)
        with conn.cursor() as cur:
            # Normalizar nombre en MAYÚSCULAS para persistencia consistente
            try:
                nombre = (nombre or '').strip().upper()
            except Exception:
                nombre = str(nombre).upper() if nombre is not None else ''
            # 1) Upsert en tabla objetos (asegurar id = channel)
            try:
                cur.execute(
                    """
                    INSERT INTO objetos (id, objeto, potencia_w, consumo_wh)
                    VALUES (%s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE objeto=VALUES(objeto), potencia_w=VALUES(potencia_w), consumo_wh=VALUES(consumo_wh)
                    """,
                    (int(channel), nombre, potencia, consumo)
                )
            except Exception as e:
                # Si no existe la tabla o columnas, ignorar silenciosamente para no romper creación en entornos sin esquema completo
                print(f"Aviso: no se pudo upsert en objetos: {e}")

            # 2) Insert/Update en tabla leds (para color y metadatos)
            cur.execute(
                """
                INSERT INTO leds (channel, nombre, potencia, consumo, color)
                VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE nombre=VALUES(nombre), potencia=VALUES(potencia), consumo=VALUES(consumo), color=VALUES(color)
                """,
                (channel, nombre, potencia, consumo, color)
            )
            new_id = cur.lastrowid
        conn.commit()
        conn.close()
        return new_id
