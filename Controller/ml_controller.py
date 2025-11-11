# Controller ML usando modelo real con LinearRegression
import numpy as np
from Model.energia_model import EnergiaModel
from Model.ml_model import MLModel
import os

class MLController:
    
    def __init__(self):
        self.energia_model = EnergiaModel()
        self.ml_model = MLModel()
        
    def predecir_recibo_mensual(self):
        """Predicción usando modelo"""
        try:
            # Obtener datos para entrenar/predecir
            datos = self.energia_model.obtener_datos()
            
            if len(datos) < 3:  # Necesitamos al menos 3 datos para entrenar
                return self._respaldo_prediccion()
            
            # X = mes, Y = gasto total del mes
            X = np.array([[float(d['mes'])] for d in datos])
            y = np.array([float(d['gasto_total']) for d in datos])
            
            # Intentar cargar modelo existente primero
            try:
                modelo = self.ml_model.cargar_modelo()
            except (FileNotFoundError, Exception):
                # Si no existe modelo, entrenar uno nuevo
                self.ml_model.entrenar_modelo(X, y)
                modelo = self.ml_model.model
            
            # Predecir el gasto del próximo mes
            import datetime
            mes_actual = datetime.datetime.now().month
            proximo_mes = mes_actual + 1 if mes_actual < 12 else 1
            entrada_proximo_mes = np.array([[proximo_mes]])
            
            # Realizar predicción con ML
            prediccion = self.ml_model.predecir(entrada_proximo_mes)[0]
            
            return {
                'prediccion_mensual': round(prediccion, 2),
                'metodo': 'machine_learning',
                'exitoso': True,
                'datos_entrenamiento': len(datos),
            }
            
        except Exception as e:
            print(f"Error en ML: {e}")
            return self._respaldo_prediccion()

    def _respaldo_prediccion(self):
        """Predicción básica cuando falla el ML"""
        try:
            # Usar gasto del mes actual si existe
            gasto_mes = self.energia_model.obtener_gasto_mes()
            if gasto_mes > 1000:
                return {
                    'prediccion_mensual': round(gasto_mes * 1.1, 2),
                    'metodo': 'fallback_basico',
                    'exitoso': True,
                    'datos_entrenamiento': 0
                }
            
            # Si no hay gasto del mes, usar promedio por uso
            consumo_promedio = self.energia_model.obtener_consumo()
            prediccion = consumo_promedio * 60  # 60 usos estimados por mes
            
            return {
                'prediccion_mensual': round(prediccion, 2),
                'metodo': 'fallback_basico',
                'exitoso': True,
                'datos_entrenamiento': 0
            }
        except:
            return {
                'prediccion_mensual': 45000.0,
                'metodo': 'valor_defecto',
                'exitoso': True
            }