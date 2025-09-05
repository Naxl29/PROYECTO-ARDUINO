# Controlador para gestionar el modelo ML y el seguimiento del consumo energético

import os
import numpy as np
from datetime import datetime
import logging
from threading import Lock

# Importa las clases del proyecto
from Model.ml_model import MLModel
from Model.database import Database
from Model.reporte import Reporte
from config.ml_config import MODEL_PATH
from config.roles_config import LED_NAMES

# Configura logging para mensajes informativos
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MiController:
    #Controlador para la gestión del modelo ML y el seguimiento del consumo energético
    def __init__(self):
        self.ml_model = MLModel()
        self.db = Database()
        self.reporte_model = Reporte() # Instancia para guardar los reportes
        self.min_data_points = 12 # Número mínimo de puntos para entrenar el modelo
        
        # Diccionario para almacenar el estado y consumo de cada bombilla
        self.estado_bombillas = {}
        # Usa un candado para manejar el acceso concurrente a los datos de las bombillas
        self._lock = Lock()
        
        # Definir la tarifa del estrato 4
        self.TARIFA_COP_KWH = 1000 # Precio por kWh para el Estrato 4, según tu tabla.
        
        # Mapeo de IDs de Arduino a IDs de la base de datos
        self._mapeo_id_arduino_a_db = {
            "LUZ SALA": 1, 
            "LED 1": 2, 
            "LED 2": 3,
            "LED 3": 4, 
            "LED 4": 5, 
            "LED 5": 6, 
            "LED 6": 7, 
            "LED 7": 8
        }
        
        # Verifica si el modelo ya está entrenado si no, lo entrena
        if not os.path.exists(MODEL_PATH):
            logging.warning("El modelo ML no existe. Se intentará entrenar.")
            self.entrenar_modelo_inicial()
        else:
            logging.info("El modelo ML ya existe. Se cargará para su uso.")
            self.ml_model.cargar_modelo()

    def entrenar_modelo_inicial(self):
        """
        Entrena el modelo ML si no existe. 
        Utiliza datos históricos desde la base de datos (o simulados para el primer uso).
        """
        try:
            datos_historicos = self.db.obtener_datos_historicos()

            if len(datos_historicos) >= self.min_data_points:
                X = np.array([[d[0]] for d in datos_historicos]) # Mes del año como feature
                y = np.array([d[1] for d in datos_historicos]) # Consumo como target
                
                self.ml_model.entrenar_modelo(X, y)
                logging.info("Modelo entrenado exitosamente con datos históricos.")
                return True
            else:
                logging.warning(
                    f"No hay suficientes datos históricos para entrenar el modelo. "
                    f"Se necesitan al menos {self.min_data_points} puntos."
                )
                return False

        except Exception as e:
            logging.error(f" Error al entrenar el modelo: {e}")
            return False

    # Se agregó el argumento 'duracion_s' para recibir los segundos del Arduino
    def manejar_evento_bombilla(self, bombilla_id: str, estado: bool, duracion_s: float, consumo_w: float):
        """
        Maneja un evento de cambio de estado de una bombilla y actualiza el consumo.

        Args:
            bombilla_id (str): Identificador único de la bombilla (ej. "led_1").
            estado (bool): True si está encendida, False si está apagada.
            duracion_s (float): El tiempo en segundos que el dispositivo estuvo encendido.
            consumo_w (float): El consumo de la bombilla en vatios (W).
        """
        with self._lock:
            # Actualiza el estado y consumo de la bombilla en el diccionario
            self.estado_bombillas[bombilla_id] = {
                'estado': estado,
                'consumo': consumo_w,
                'duracion_s': duracion_s
            }
        
        # Calular la duración real en minutos
        duracion_minutos = duracion_s * 10
        
        # Calcular el consumo en kWh para el evento
        consumo_kwh = (consumo_w * duracion_minutos) / 60 / 1000
        
        # Calcular el gasto en pesos colombianos
        gasto_cop = consumo_kwh * self.TARIFA_COP_KWH
        
        logging.info(f"💡 Evento: Bombilla {bombilla_id} se ha {'encendido' if estado else 'apagado'} "
                    f"con un consumo de {consumo_w} W y un gasto de ${gasto_cop:,.2f} COP.")
        
        # Guardar el evento en la base de datos
        # Aquí debes determinar el id_usuario y el id_objeto
        id_usuario = 1 # O un valor dinámico si la app lo provee
        id_objeto = self._mapeo_id_arduino_a_db.get(bombilla_id)
        
        if id_objeto:
            self.reporte_model.save(id_usuario, id_objeto, duracion_minutos, estado, gasto_cop)
            logging.info(f" Evento guardado en la base de datos para el objeto {id_objeto}.")
        else:
            logging.error(f" Error: ID de objeto '{bombilla_id}' no encontrado en el mapeo.")

    def obtener_consumo_actual_total(self):
        #Calcula el consumo total de todas las bombillas encendidas.
        """
        Returns:
            float: El consumo total actual en vatios (W).
        """
        consumo_total = 0.0
        with self._lock:
            for bombilla in self.estado_bombillas.values():
                if bombilla['estado']:
                    consumo_total += bombilla['consumo']
        
        logging.info(f"Consumo total actual detectado: {consumo_total:.2f} W")
        return consumo_total
        
    def predecir_consumo_proximo_mes(self):
        # Predice el valor del consumo para el próximo mes.
        try:
            mes_actual = datetime.now().month
            proximo_mes = 1 if mes_actual == 12 else mes_actual + 1
            
            entrada = np.array([[proximo_mes]])
            prediccion = self.ml_model.predecir(entrada)[0]
            
            logging.info(f"🔮 Predicción para el mes {proximo_mes}: ${prediccion:,.2f}")
            return prediccion
            
        except Exception as e:
            logging.error(f"Error al realizar la predicción: {e}")
            return None