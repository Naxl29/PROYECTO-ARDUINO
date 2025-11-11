from __future__ import annotations

from typing import Sequence, Tuple

import pymysql
from pymysql.connections import Connection
from pymysql.cursors import DictCursor

from Model.database import Database


class DatabaseInitializationError(RuntimeError):
    pass


class DatabaseSeedError(RuntimeError):
    pass


def _schema_statements() -> Sequence[str]:
    return (
        """
        CREATE TABLE IF NOT EXISTS usuarios (
            id INT NOT NULL AUTO_INCREMENT,
            usuario VARCHAR(50) NOT NULL,
            contrasena VARCHAR(50) NOT NULL,
            PRIMARY KEY (id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
        """,
        """
        CREATE TABLE IF NOT EXISTS objetos (
            id INT NOT NULL AUTO_INCREMENT,
            objeto VARCHAR(50) NOT NULL,
            potencia_w INT NOT NULL,
            consumo_wh FLOAT NOT NULL,
            color VARCHAR(7) NOT NULL DEFAULT '#ffffff',
            PRIMARY KEY (id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
        """,
        """
        CREATE TABLE IF NOT EXISTS roles (
            id INT NOT NULL AUTO_INCREMENT,
            rol VARCHAR(50) NOT NULL,
            PRIMARY KEY (id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
        """,
        """
        CREATE TABLE IF NOT EXISTS reportes (
            id INT NOT NULL AUTO_INCREMENT,
            id_usuario INT NOT NULL,
            id_objeto INT NOT NULL,
            fecha DATETIME NOT NULL,
            duracion_minutos FLOAT NOT NULL,
            estado TINYINT(1) NOT NULL,
            gasto FLOAT NOT NULL,
            PRIMARY KEY (id),
            KEY FK_reportes_usuarios (id_usuario),
            KEY FK_reportes_objetos (id_objeto),
            CONSTRAINT FK_reportes_objetos FOREIGN KEY (id_objeto) REFERENCES objetos(id),
            CONSTRAINT FK_reportes_usuarios FOREIGN KEY (id_usuario) REFERENCES usuarios(id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
        """,
        """
        CREATE TABLE IF NOT EXISTS roles_usuarios (
            id INT NOT NULL AUTO_INCREMENT,
            id_usuario INT NOT NULL,
            id_rol INT NOT NULL,
            PRIMARY KEY (id),
            KEY FK_ru_usuarios (id_usuario),
            KEY FK_ru_roles (id_rol),
            CONSTRAINT FK_ru_roles FOREIGN KEY (id_rol) REFERENCES roles(id),
            CONSTRAINT FK_ru_usuarios FOREIGN KEY (id_usuario) REFERENCES usuarios(id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
        """,
        """
        CREATE TABLE IF NOT EXISTS secciones (
            id INT NOT NULL AUTO_INCREMENT,
            nombre VARCHAR(60) NOT NULL UNIQUE,
            suspendida TINYINT(1) NOT NULL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
        """,
        """
        CREATE TABLE IF NOT EXISTS dispositivo_secciones (
            channel VARCHAR(10) NOT NULL PRIMARY KEY,
            section_id INT NOT NULL,
            assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT fk_dispositivo_secciones FOREIGN KEY (section_id) REFERENCES secciones(id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
        """,
        """
        CREATE TABLE IF NOT EXISTS secciones_roles (
            section_id INT NOT NULL,
            role VARCHAR(20) NOT NULL,
            PRIMARY KEY (section_id, role),
            CONSTRAINT fk_secciones_roles FOREIGN KEY (section_id) REFERENCES secciones(id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
        """,
        """
        CREATE TABLE IF NOT EXISTS device_flags (
            channel VARCHAR(10) NOT NULL PRIMARY KEY,
            suspendido TINYINT(1) NOT NULL DEFAULT 0,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
        """,
    )


def _column_definitions() -> Sequence[Tuple[str, str, str]]:
    return (
        ("objetos", "color", "`color` VARCHAR(7) NOT NULL DEFAULT '#ffffff'"),
        ("secciones", "suspendida", "`suspendida` TINYINT(1) NOT NULL DEFAULT 0"),
    )


def initialize_schema() -> None:
    database = Database()
    connection = database.conexion()
    try:
        _execute_schema_statements(connection)
        _ensure_columns(connection, database.database)
        connection.commit()
    except pymysql.MySQLError as error:
        connection.rollback()
        raise DatabaseInitializationError(f"No se pudo inicializar el esquema: {error}") from error
    finally:
        connection.close()


def _execute_schema_statements(connection: Connection) -> None:
    with connection.cursor() as cursor:
        for statement in _schema_statements():
            cursor.execute(statement)


def _ensure_columns(connection: Connection, schema_name: str) -> None:
    with connection.cursor() as cursor:
        for table_name, column_name, definition in _column_definitions():
            cursor.execute(
                """
                SELECT COUNT(*) AS total
                FROM information_schema.COLUMNS
                WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s AND COLUMN_NAME = %s
                """,
                (schema_name, table_name, column_name),
            )
            row = cursor.fetchone()
            exists = bool(row and row.get("total"))
            if not exists:
                cursor.execute(f"ALTER TABLE `{table_name}` ADD COLUMN {definition}")


def seed_default_data() -> None:
    database = Database()
    connection = database.conexion()
    try:
        with connection.cursor() as cursor:
            _seed_default_users(cursor)
            _seed_default_objects(cursor)
            _seed_default_roles(cursor)
            _seed_default_roles_usuarios(cursor)
        connection.commit()
    except pymysql.MySQLError as error:
        connection.rollback()
        raise DatabaseSeedError(f"No se pudieron insertar los datos por defecto: {error}") from error
    finally:
        connection.close()


def _seed_default_users(cursor: DictCursor) -> None:
    cursor.execute("SELECT COUNT(*) AS total FROM usuarios")
    row = cursor.fetchone()
    has_data = bool(row and row.get("total"))
    if not has_data:
        cursor.execute(
            """
            INSERT INTO usuarios (id, usuario, contrasena) VALUES
            (1, 'ADMIN', '123456'),
            (2, 'USER', '123456'),
            (3, 'CHILD', '123456')
            """
        )


def _seed_default_objects(cursor: DictCursor) -> None:
    cursor.execute("SELECT COUNT(*) AS total FROM objetos")
    row = cursor.fetchone()
    has_data = bool(row and row.get("total"))
    if not has_data:
        cursor.execute(
            """
            INSERT INTO objetos (id, objeto, potencia_w, consumo_wh, color) VALUES
            (1, 'LUZ SALA', 60, 0.06, '#ff4444'),
            (2, 'LUZ COCINA', 60, 0.06, '#44ff44'),
            (3, 'LUZ HABITACIÓN', 60, 0.06, '#4444ff'),
            (4, 'LUZ BAÑO', 60, 0.06, '#ffff44'),
            (5, 'AIRE ACONDICIONADO', 800, 0.8, '#ff44ff'),
            (6, 'LAVADORA', 500, 0.5, '#44ffff'),
            (7, 'NEVERA', 200, 0.2, '#ff8c00'),
            (8, 'TELEVISOR', 150, 0.15, '#8a2be2'),
            (9, 'BOMBILLO', 60, 0.06, '#ffffff')
            """
        )


def _seed_default_roles(cursor: DictCursor) -> None:
    cursor.execute("SELECT COUNT(*) AS total FROM roles")
    row = cursor.fetchone()
    has_data = bool(row and row.get("total"))
    if not has_data:
        cursor.execute(
            """
            INSERT INTO roles (id, rol) VALUES
            (1, 'ADMIN'),
            (2, 'USER'),
            (3, 'CHILD')
            """
        )


def _seed_default_roles_usuarios(cursor: DictCursor) -> None:
    cursor.execute("SELECT COUNT(*) AS total FROM roles_usuarios")
    row = cursor.fetchone()
    has_data = bool(row and row.get("total"))
    if not has_data:
        cursor.execute(
            """
            INSERT INTO roles_usuarios (id, id_usuario, id_rol) VALUES
            (1, 1, 1),
            (2, 2, 2),
            (3, 3, 3)
            """
        )

