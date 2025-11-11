from typing import Dict
from Model.database import Database


class DeviceFlagsModel:
    TABLE_SQL = (
        """
        CREATE TABLE IF NOT EXISTS device_flags (
            channel VARCHAR(10) NOT NULL PRIMARY KEY,
            suspendido TINYINT(1) NOT NULL DEFAULT 0,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
    )

    @staticmethod
    def _ensure_table(conn) -> None:
        with conn.cursor() as cur:
            cur.execute(DeviceFlagsModel.TABLE_SQL)

    @staticmethod
    def set_suspended(channel: str, suspended: bool) -> None:
        conn = Database().conexion()
        DeviceFlagsModel._ensure_table(conn)
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO device_flags (channel, suspendido)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE suspendido=VALUES(suspendido)
                """,
                (str(channel), 1 if suspended else 0)
            )
        conn.commit()
        conn.close()

    @staticmethod
    def is_suspended(channel: str) -> bool:
        conn = Database().conexion()
        DeviceFlagsModel._ensure_table(conn)
        with conn.cursor() as cur:
            cur.execute("SELECT suspendido FROM device_flags WHERE channel=%s", (str(channel),))
            row = cur.fetchone()
        conn.close()
        return bool(row and row.get('suspendido'))

    @staticmethod
    def get_flags_map() -> Dict[str, bool]:
        conn = Database().conexion()
        DeviceFlagsModel._ensure_table(conn)
        with conn.cursor() as cur:
            cur.execute("SELECT channel, suspendido FROM device_flags")
            rows = cur.fetchall() or []
        conn.close()
        return {str(r['channel']): bool(r.get('suspendido')) for r in rows}

    @staticmethod
    def clear(channel: str) -> None:
        conn = Database().conexion()
        DeviceFlagsModel._ensure_table(conn)
        with conn.cursor() as cur:
            cur.execute("DELETE FROM device_flags WHERE channel=%s", (str(channel),))
        conn.commit()
        conn.close()
