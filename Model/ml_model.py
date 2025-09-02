import pickle
import numpy as np
from sklearn.linear_model import LinearRegression
from config.ml_config import MODEL_PATH # Variable de entorno que guarda la ruta donde se almacena el modelo

class MLModel:
    def __init__(self):
        self.model_path = MODEL_PATH 
        self.model = None

    def entrenar_modelo(self, X, y): # Funcion que entrena el modelo ML
        modelo = LinearRegression()
        modelo.fit(X, y)
        self.model = modelo

        with open(self.model_path, "wb") as f:
            pickle.dump(modelo, f) # Guardar el modelo en un archivo

        return modelo # Retorna el modelo entrenado

    def cargar_modelo(self): # Cargar el modelo desde un archivo
        if self.model is None:
            with open(self.model_path, "rb") as f:
                self.model = pickle.load(f) # Cargar el modelo desde el archivo
        return self.model # Retorna el modelo cargado

    def predecir(self, entrada): # Realiza predicciones usando el modelo cargado
        modelo = self.cargar_modelo()
        return modelo.predict(entrada) # Retorna las predicciones
