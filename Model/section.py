from typing import List, Dict, Optional
from Model.database import Database


class SectionModel:
    @staticmethod
    def list_sections() -> List[Dict]:
        conn = Database().conexion()
        with conn.cursor() as cur:
            cur.execute("SELECT id, nombre, suspendida FROM secciones ORDER BY nombre ASC")
            rows = cur.fetchall() or []
        conn.close()
        return rows

    @staticmethod
    def list_sections_with_roles() -> List[Dict]:
        conn = Database().conexion()
        with conn.cursor() as cur:
            cur.execute("SELECT id, nombre, suspendida FROM secciones ORDER BY nombre ASC")
            sections = cur.fetchall() or []
            # Obtener roles agrupados por sección
            cur.execute("SELECT section_id, role FROM secciones_roles")
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
        with conn.cursor() as cur:
            nombre_up = (nombre or '').strip().upper()
            cur.execute("UPDATE secciones SET nombre=%s WHERE id=%s", (nombre_up, int(section_id)))
        conn.commit()
        conn.close()

    @staticmethod
    def set_suspended(section_id: int, suspended: bool) -> None:
        conn = Database().conexion()
        with conn.cursor() as cur:
            # Actualizar estado de la sección
            cur.execute("UPDATE secciones SET suspendida=%s WHERE id=%s", (1 if suspended else 0, int(section_id)))
            
            # Suspender/activar todos los dispositivos asignados a esta sección
            cur.execute("SELECT channel FROM dispositivo_secciones WHERE section_id=%s", (int(section_id),))
            channels = [row['channel'] for row in cur.fetchall() or []]
            
            # Actualizar flags de dispositivos en cascada
            for channel in channels:
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
    def delete_section(section_id: int) -> None:
        conn = Database().conexion()
        with conn.cursor() as cur:
            # Obtener dispositivos asignados antes de eliminar
            cur.execute("SELECT channel FROM dispositivo_secciones WHERE section_id=%s", (int(section_id),))
            channels = [row['channel'] for row in cur.fetchall() or []]

            # Eliminar sección (esto eliminará dispositivo_secciones por FK CASCADE)
            cur.execute("DELETE FROM secciones WHERE id=%s", (int(section_id),))
            
            # Limpiar flags de suspensión de dispositivos que estaban en esta sección
            for channel in channels:
                cur.execute("DELETE FROM device_flags WHERE channel=%s", (str(channel),))
        conn.commit()
        conn.close()

    @staticmethod
    def assign_device(channel: str, section_id: int) -> None:
        conn = Database().conexion()
        with conn.cursor() as cur:
            # Asignar dispositivo a sección
            cur.execute(
                """
                INSERT INTO dispositivo_secciones (channel, section_id)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE section_id=VALUES(section_id)
                """,
                (str(channel), int(section_id))
            )
            
            # Si la sección está suspendida, suspender automáticamente el dispositivo
            cur.execute("SELECT suspendida FROM secciones WHERE id=%s", (int(section_id),))
            section_row = cur.fetchone()
            if section_row and section_row.get('suspendida'):
                cur.execute(
                    """
                    INSERT INTO device_flags (channel, suspendido)
                    VALUES (%s, 1)
                    ON DUPLICATE KEY UPDATE suspendido=1
                    """,
                    (str(channel),)
                )
        conn.commit()
        conn.close()

    @staticmethod
    def remove_assignment(channel: str) -> None:
        conn = Database().conexion()
        with conn.cursor() as cur:
            # Eliminar asignación
            cur.execute("DELETE FROM dispositivo_secciones WHERE channel=%s", (str(channel),))
            
            # Limpiar flag de suspensión del dispositivo al quitarlo de la sección
            cur.execute("DELETE FROM device_flags WHERE channel=%s", (str(channel),))
        conn.commit()
        conn.close()

    @staticmethod
    def get_device_sections_map() -> Dict[str, Dict]:
        """Return mapping channel -> {id, nombre, roles: [..]} for quick lookups."""
        conn = Database().conexion()
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT ds.channel as channel, s.id as id, s.nombre as nombre
                FROM dispositivo_secciones ds
                JOIN secciones s ON s.id = ds.section_id
                """
            )
            rows = cur.fetchall() or []
            # roles por sección
            cur.execute("SELECT section_id, role FROM secciones_roles")
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
        roles = [str(x).upper() for x in (roles or [])]
        with conn.cursor() as cur:
            # Eliminar roles no incluidos
            if roles:
                cur.execute(
                    "DELETE FROM secciones_roles WHERE section_id=%s AND role NOT IN (%s)" % (
                        "%s",
                        ",".join(["%s"] * len(roles))
                    ),
                    tuple([int(section_id)] + roles)
                )
            else:
                cur.execute("DELETE FROM secciones_roles WHERE section_id=%s", (int(section_id),))
            # Insertar roles faltantes
            for role in roles:
                cur.execute(
                    """
                    INSERT IGNORE INTO secciones_roles (section_id, role)
                    VALUES (%s, %s)
                    """,
                    (int(section_id), role)
                )
        conn.commit()
        conn.close()
