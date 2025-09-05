# Controller simple para predicciones ML
import numpy as np
from Model.ml_model import MLModel
from Model.energia_model import EnergiaModel

class MLController:
    
    def __init__(self):
        self.ml_model = MLModel()
        self.energia_model = EnergiaModel()
        
    def predecir_recibo(self, consumo=None):
        """Predice el costo del recibo"""
        if consumo is None:
            consumo = self.energia_model.obtener_consumo()
        
        entrada = np.array([[consumo]])
        prediccion = self.ml_model.predecir(entrada)
        
        return {
            'prediccion': round(prediccion[0], 2),
            'consumo': consumo,
            'exitoso': True
        }
    
    def entrenar_modelo(self):
        """Entrena el modelo con datos"""
        datos = self.energia_model.obtener_datos()
        
        X = np.array([[float(row['consumo_kwh'])] for row in datos])
        y = np.array([float(row['costo']) for row in datos])
        
        self.ml_model.entrenar_modelo(X, y)
        return {'exitoso': True, 'mensaje': f'Entrenado con {len(datos)} registros'}