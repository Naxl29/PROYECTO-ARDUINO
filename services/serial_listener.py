#Archivo que escucha datos del arduino y los procesa
import serial
import json
import time
import sys
import os
import logging
from datetime import datetime

# Agregar la ruta del proyecto al path de Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

try:
    from Controller.ml_controller import MiController
except ImportError as e:
    logging.error(f"Error al importar MiController: {e}")
    logging.error("Asegúrate de que la ruta del proyecto esté en el PYTHONPATH.")
    sys.exit(1)

# CONFIGURACIÓN

SERIAL_PORT = "COM3"  # Ajustar puerto. "
BAUD_RATE = 9600

# Gestion de eventos de bombillas
def procesar_dato_arduino(line: str, controller: MiController):
    try:
        if not line.startswith('{'):
            logging.warning("El formato de datos no es JSON. Asegúrate de que el Arduino lo envíe así.")
            return

        data = json.loads(line)
        
        if 'id' in data and 'estado' in data and 'consumo' in data:
            bombilla_id = data['id']
            estado = data['estado']
            consumo = data['consumo']
            
            controller.manejar_evento_bombilla(bombilla_id, estado, consumo)
            
        else:
            logging.error(f"Datos incompletos o incorrectos recibidos: {data}")

    except json.JSONDecodeError:
        logging.error(f"Error de formato JSON en la línea: {line}")
    except Exception as e:
        logging.error(f"Error procesando datos: {e}")

# Función principal
def main():
    controller = MiController()
    try:
        logging.info(f"Conectando a {SERIAL_PORT} a {BAUD_RATE} baudios...")
        arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)

        logging.info("Conectado a Arduino. cargando datos...")

        while True:
            if arduino.in_waiting > 0:
                line = arduino.readline().decode("utf-8").strip()
                if line:
                    logging.info(f"Recibido de Arduino: {line}")
                    procesar_dato_arduino(line, controller)

    except serial.SerialException as e:
        logging.error(f"No se pudo abrir el puerto serial {SERIAL_PORT}: {e}")
    except KeyboardInterrupt:
        logging.info("\nListener detenido manualmente.")
    finally:
        if 'arduino' in locals() and arduino.is_open:
            arduino.close()
            logging.info("Conexión serial cerrada.")

if __name__ == "__main__":
    main()