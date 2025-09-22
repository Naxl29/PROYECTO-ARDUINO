import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class Config:   
    # Base de datos
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_DATABASE = os.getenv('DB_DATABASE', 'arduino')
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    
    # Flask
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', os.urandom(24))
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    # Arduino
    ARDUINO_IP = os.getenv('ARDUINO_IP', '10.7.61.17')
    # 10.7.61.17 SENA
    # 192.168.101.77 CASA LISSETH
    # 192.168.101.74 CASA CARLOS

    BASE_URL = f"http://{ARDUINO_IP}/"
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'app.log')

class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True

class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False

# Configuración por defecto
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
