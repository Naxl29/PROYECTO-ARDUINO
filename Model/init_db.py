"""
Módulo de inicialización automática de la base de datos.
Crea todas las tablas necesarias al iniciar la aplicación.
"""
from Model.database import Database


class DatabaseInitializer:
    """Clase para inicializar todas las tablas de la base de datos automáticamente."""
    
    # Tablas básicas del sistema
    USUARIOS_SQL = """
        CREATE TABLE IF NOT EXISTS usuarios (
            id INT NOT NULL AUTO_INCREMENT,
            usuario VARCHAR(50) NOT NULL,
            contrasena VARCHAR(50) NOT NULL,
            PRIMARY KEY (id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
    """
    
    OBJETOS_SQL = """
        CREATE TABLE IF NOT EXISTS objetos (
            id INT NOT NULL AUTO_INCREMENT,
            objeto VARCHAR(50) NOT NULL,
            potencia_w INT NOT NULL,
            consumo_wh FLOAT NOT NULL,
            color VARCHAR(7) DEFAULT '#ffffff',
            PRIMARY KEY (id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
    """
    
    REPORTES_SQL = """
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
    """
    
    ROLES_SQL = """
        CREATE TABLE IF NOT EXISTS roles (
            id INT NOT NULL AUTO_INCREMENT,
            rol VARCHAR(50) NOT NULL,
            PRIMARY KEY (id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
    """
    
    ROLES_USUARIOS_SQL = """
        CREATE TABLE IF NOT EXISTS roles_usuarios (
            id INT NOT NULL AUTO_INCREMENT,
            id_usuario INT NOT NULL,
            id_rol INT NOT NULL,
            PRIMARY KEY (id),
            KEY FK__usuarios (id_usuario),
            KEY FK__roles (id_rol),
            CONSTRAINT FK__roles FOREIGN KEY (id_rol) REFERENCES roles(id),
            CONSTRAINT FK__usuarios FOREIGN KEY (id_usuario) REFERENCES usuarios(id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
    """
    
    @staticmethod
    def initialize_all_tables():
        """
        Inicializa todas las tablas de la base de datos.
        Se ejecuta automáticamente al iniciar la aplicación.
        """
        try:
            db = Database()
            conn = db.conexion()
            
            with conn.cursor() as cur:
                # Crear tablas básicas (en orden de dependencias)
                print("🔄 Inicializando tablas de la base de datos...")
                
                # 1. Tablas básicas sin dependencias
                print("  📋 Creando tabla: usuarios")
                cur.execute(DatabaseInitializer.USUARIOS_SQL)
                
                print("  📋 Creando tabla: objetos")
                cur.execute(DatabaseInitializer.OBJETOS_SQL)
                
                print("  📋 Creando tabla: roles")
                cur.execute(DatabaseInitializer.ROLES_SQL)
                
                # 2. Tablas con dependencias
                print("  📋 Creando tabla: reportes")
                cur.execute(DatabaseInitializer.REPORTES_SQL)
                
                print("  📋 Creando tabla: roles_usuarios")
                cur.execute(DatabaseInitializer.ROLES_USUARIOS_SQL)
                
                # 3. Tablas que se crean automáticamente por otros modelos
                # (secciones, dispositivo_secciones, secciones_roles, device_flags)
                # Estas se crearán automáticamente cuando se usen por primera vez
                
                # Asegurar que la columna 'color' existe en objetos
                try:
                    print("  🔧 Verificando columna 'color' en tabla objetos...")
                    cur.execute("ALTER TABLE objetos ADD COLUMN color VARCHAR(7) DEFAULT '#ffffff'")
                    print("    ✅ Columna 'color' agregada")
                except Exception:
                    # La columna ya existe, continuar
                    pass
                
            conn.commit()
            conn.close()
            
            print("✅ Inicialización de base de datos completada exitosamente")
            return True
            
        except Exception as e:
            print(f"❌ Error al inicializar la base de datos: {e}")
            print(f"   Detalles: {str(e)}")
            # No lanzar excepción para permitir que la app continúe
            # Las tablas se crearán cuando se usen por primera vez
            return False
    
    @staticmethod
    def insert_default_data():
        """
        Inserta datos por defecto si las tablas están vacías.
        Solo se ejecuta si se necesita (opcional).
        """
        try:
            db = Database()
            conn = db.conexion()
            
            with conn.cursor() as cur:
                # Verificar si ya existen datos (con manejo de errores)
                try:
                    cur.execute("SELECT COUNT(*) as count FROM usuarios")
                    usuarios_count = cur.fetchone()['count']
                except Exception:
                    usuarios_count = 0
                
                try:
                    cur.execute("SELECT COUNT(*) as count FROM objetos")
                    objetos_count = cur.fetchone()['count']
                except Exception:
                    objetos_count = 0
                
                try:
                    cur.execute("SELECT COUNT(*) as count FROM roles")
                    roles_count = cur.fetchone()['count']
                except Exception:
                    roles_count = 0
                
                # Solo insertar si las tablas están vacías
                if usuarios_count == 0:
                    print("  📝 Insertando usuarios por defecto...")
                    cur.execute("""
                        INSERT INTO usuarios (id, usuario, contrasena) VALUES
                        (1, 'ADMIN', '123456'),
                        (2, 'USER', '123456'),
                        (3, 'CHILD', '123456')
                    """)
                
                if objetos_count == 0:
                    print("  📝 Insertando objetos por defecto...")
                    cur.execute("""
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
                    """)
                
                if roles_count == 0:
                    print("  📝 Insertando roles por defecto...")
                    cur.execute("""
                        INSERT INTO roles (id, rol) VALUES
                        (1, 'ADMIN'),
                        (2, 'USER'),
                        (3, 'CHILD')
                    """)
                    
                    # Asignar roles a usuarios
                    cur.execute("""
                        INSERT INTO roles_usuarios (id, id_usuario, id_rol) VALUES
                        (1, 1, 1),
                        (2, 2, 2),
                        (3, 3, 3)
                    """)
                
            conn.commit()
            conn.close()
            
            print("✅ Datos por defecto insertados correctamente")
            return True
            
        except Exception as e:
            print(f"⚠️  Advertencia al insertar datos por defecto: {e}")
            return False

