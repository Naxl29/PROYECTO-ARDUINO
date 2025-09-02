import joblib
import numpy as np
import pandas as pd

# ----------------------------
# Cargar modelo entrenado
# ----------------------------
modelo = joblib.load("modelo.pkl")

# Tarifa fija (estrato 4 = 1000 COP/kWh)
tarifa = 1000

def predecir_consumo(potencia, tiempo):
    """
    Predice el consumo en kWh dado:
    - potencia (W)
    - tiempo (minutos)
    """
    X = pd.DataFrame([[potencia, tiempo, ]], columns=["potencia", "tiempo",])
    consumo_pred = modelo.predict(X)[0]
    return max(consumo_pred, 0.0001)

def predecir_costo(potencia, tiempo):
    """
    Predice el costo en COP (estrato fijo = 4).
    """
    consumo = predecir_consumo(potencia, tiempo)
    return consumo * tarifa

# ----------------------------
# Ejemplo de uso
# ----------------------------
if __name__ == "__main__":
    potencia = 60   # Bombilla 60W
    tiempo = 120    # 2 horas (120 minutos)

    consumo = predecir_consumo(potencia, tiempo)
    costo = predecir_costo(potencia, tiempo)

    print(f"⚡ Consumo estimado: {consumo:.4f} kWh")
    print(f"💰 Costo estimado (estrato 4): {costo:.2f} COP")
    print("✅ Modelo cargado y listo para predecir")