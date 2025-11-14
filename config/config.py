import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class Config:   
    # Base de datos
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = int(os.getenv('DB_PORT', '3306'))
    DB_DATABASE = os.getenv('DB_DATABASE', 'arduino')
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    
    # Flask
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', os.urandom(24))
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    # Arduino
    ARDUINO_IP = os.getenv('ARDUINO_IP', '10.220.159.1')
    # 10.220.159.1 CELULAR NICOLÁS
    # 10.38.81.1 CELULAR CARLOS
    # 10.7.53.40 SENA
    # 192.168.101.77 CASA LISSETH
    # 192.168.101.74 CASA CARLOS

    BASE_URL = f"http://{ARDUINO_IP}/"
    HARDWARE_API_TOKEN = os.getenv('HARDWARE_API_TOKEN', '')
    HARDWARE_DEFAULT_USER_ID = int(os.getenv('HARDWARE_DEFAULT_USER_ID', '1'))
    
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
