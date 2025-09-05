import serial
import requests
import json
import time

# -------------------------
# CONFIGURACIÓN
# -------------------------
SERIAL_PORT = "COM3"   # Ajustar según el puerto de tu Arduino ("/dev/ttyUSB0")
BAUD_RATE = 9600
FLASK_URL = "http://127.0.0.1:5000/predict"  # Tu servidor Flask

# -------------------------
# ESCUCHAR SERIAL
# -------------------------
def main():
    try:
        print(f"Conectando a {SERIAL_PORT} a {BAUD_RATE} baudios...")
        arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)  # Esperar a que Arduino reinicie

        print(" Conectado a Arduino. Escuchando datos...")

        while True:
            if arduino.in_waiting > 0:
                line = arduino.readline().decode("utf-8").strip()

                if line:
                    print(f"Recibido de Arduino: {line}")

                    try:
                        # Esperamos que Arduino mande algo como: "potencia:200,tiempo:120"
                        data = json.loads(line) if line.startswith("{") else None
                        if not data:
                            # Parseo manual si es "potencia=200,tiempo=120"
                            parts = line.split(",")
                            data = {
                                "potencia": float(parts[0].split("=")[1]),
                                "tiempo": float(parts[1].split("=")[1]),
                            }

                        # Llamar al endpoint Flask
                        response = requests.post(FLASK_URL, json=data)
                        if response.status_code == 200:
                            result = response.json()
                            print(f"Consumo: {result['consumo_kwh']} kWh |  Costo: {result['costo_cop']} COP")
                        else:
                            print(f" Error en Flask: {response.text}")

                    except Exception as e:
                        print(f"Error procesando línea: {line} | {e}")

    except serial.SerialException as e:
        print(f"No se pudo abrir el puerto serial {SERIAL_PORT}: {e}")
    except KeyboardInterrupt:
        print("\n Listener detenido manualmente.")

if __name__ == "__main__":
    main()
