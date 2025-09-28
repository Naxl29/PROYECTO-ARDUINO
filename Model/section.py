from typing import List, Dict, Optional
from Model.database import Database


class SectionModel:
    SECTIONS_SQL = (
        """
        CREATE TABLE IF NOT EXISTS secciones (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(60) NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
    )

    DEVICE_SECTIONS_SQL = (
        """
        CREATE TABLE IF NOT EXISTS device_sections (
            channel VARCHAR(10) NOT NULL PRIMARY KEY,
            section_id INT NOT NULL,
            assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT fk_section FOREIGN KEY (section_id) REFERENCES secciones(id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
    )

    SECTION_ROLES_SQL = (
        """
        CREATE TABLE IF NOT EXISTS section_roles (
            section_id INT NOT NULL,
            role VARCHAR(20) NOT NULL,
            PRIMARY KEY (section_id, role),
            CONSTRAINT fk_section_roles FOREIGN KEY (section_id) REFERENCES secciones(id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
    )

    @staticmethod
    def _ensure_tables(conn):
        with conn.cursor() as cur:
            cur.execute(SectionModel.SECTIONS_SQL)
            cur.execute(SectionModel.DEVICE_SECTIONS_SQL)
            cur.execute(SectionModel.SECTION_ROLES_SQL)

    @staticmethod
    def list_sections() -> List[Dict]:
        conn = Database().conexion()
        SectionModel._ensure_tables(conn)
        with conn.cursor() as cur:
            cur.execute("SELECT id, nombre FROM secciones ORDER BY nombre ASC")
            rows = cur.fetchall() or []
        conn.close()
        return rows

    @staticmethod
    def list_sections_with_roles() -> List[Dict]:
        conn = Database().conexion()
        SectionModel._ensure_tables(conn)
        with conn.cursor() as cur:
            cur.execute("SELECT id, nombre FROM secciones ORDER BY nombre ASC")
            sections = cur.fetchall() or []
            # Obtener roles agrupados por sección
            cur.execute("SELECT section_id, role FROM section_roles")
            role_rows = cur.fetchall() or []
        conn.close()
        roles_map: Dict[int, List[str]] = {}
        for r in role_rows:
            roles_map.setdefault(int(r['section_id']), []).append(r['role'])
        for s in sections:
            s['roles'] = roles_map.get(int(s['id']), [])
        return sections

    @staticmethod
    def create_section(nombre: str) -> int:
        conn = Database().conexion()
        SectionModel._ensure_tables(conn)
        with conn.cursor() as cur:
            nombre_up = (nombre or '').strip().upper()
            cur.execute("INSERT INTO secciones (nombre) VALUES (%s)", (nombre_up,))
            new_id = cur.lastrowid
        conn.commit()
        conn.close()
        return new_id

    @staticmethod
    def update_section(section_id: int, nombre: Optional[str] = None) -> None:
        if nombre is None:
            return
        conn = Database().conexion()
        SectionModel._ensure_tables(conn)
        with conn.cursor() as cur:
            nombre_up = (nombre or '').strip().upper()
            cur.execute("UPDATE secciones SET nombre=%s WHERE id=%s", (nombre_up, int(section_id)))
        conn.commit()
        conn.close()

    @staticmethod
    def assign_device(channel: str, section_id: int) -> None:
        conn = Database().conexion()
        SectionModel._ensure_tables(conn)
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO device_sections (channel, section_id)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE section_id=VALUES(section_id)
                """,
                (str(channel), int(section_id))
            )
        conn.commit()
        conn.close()

    @staticmethod
    def remove_assignment(channel: str) -> None:
        conn = Database().conexion()
        SectionModel._ensure_tables(conn)
        with conn.cursor() as cur:
            cur.execute("DELETE FROM device_sections WHERE channel=%s", (str(channel),))
        conn.commit()
        conn.close()

    @staticmethod
    def get_device_sections_map() -> Dict[str, Dict]:
        """Return mapping channel -> {id, nombre, roles: [..]} for quick lookups."""
        conn = Database().conexion()
        SectionModel._ensure_tables(conn)
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT ds.channel as channel, s.id as id, s.nombre as nombre
                FROM device_sections ds
                JOIN secciones s ON s.id = ds.section_id
                """
            )
            rows = cur.fetchall() or []
            # roles por sección
            cur.execute("SELECT section_id, role FROM section_roles")
            role_rows = cur.fetchall() or []
        conn.close()
        roles_map: Dict[int, List[str]] = {}
        for rr in role_rows:
            roles_map.setdefault(int(rr['section_id']), []).append(rr['role'])
        result: Dict[str, Dict] = {}
        for r in rows:
            result[str(r['channel'])] = {
                'id': r['id'],
                'nombre': r['nombre'],
                'roles': roles_map.get(int(r['id']), [])
            }
        return result

    @staticmethod
    def set_section_roles(section_id: int, roles: List[str]) -> None:
        conn = Database().conexion()
        SectionModel._ensure_tables(conn)
        roles = [str(x).upper() for x in (roles or [])]
        with conn.cursor() as cur:
            # Eliminar roles no incluidos
            if roles:
                cur.execute(
                    "DELETE FROM section_roles WHERE section_id=%s AND role NOT IN (%s)" % (
                        "%s",
                        ",".join(["%s"] * len(roles))
                    ),
                    tuple([int(section_id)] + roles)
                )
            else:
                cur.execute("DELETE FROM section_roles WHERE section_id=%s", (int(section_id),))
            # Insertar roles faltantes
            for role in roles:
                cur.execute(
                    """
                    INSERT IGNORE INTO section_roles (section_id, role)
                    VALUES (%s, %s)
                    """,
                    (int(section_id), role)
                )
        conn.commit()
        conn.close()
