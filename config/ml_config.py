# Configuración del modelo de Machine Learning
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Ruta del modelo entrenado desde variable de entorno
MODEL_PATH = os.getenv('MODEL_PATH', 'Model/modelo_recibo.pkl')

# Si es ruta relativa, convertir a absoluta
if not os.path.isabs(MODEL_PATH):
    MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', MODEL_PATH)

# Configuración del modelo
MODEL_ALGORITHM = os.getenv('MODEL_ALGORITHM', 'LinearRegression')

MODEL_CONFIG = {
    'algorithm': MODEL_ALGORITHM,
    'save_format': 'pickle',
    'path': MODEL_PATH
}
