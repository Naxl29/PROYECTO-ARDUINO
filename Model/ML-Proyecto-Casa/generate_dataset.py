import pandas as pd
import numpy as np

# ----------------------------
# Configuración
# ----------------------------
np.random.seed(42)  # Para reproducibilidad
n_samples = 1000    # Número de registros

# Tarifa fija (Estrato 4 = 1000 COP/kWh)
tarifa = 1000

# ----------------------------
# Generar dataset
# ----------------------------
data = []

for _ in range(n_samples):
    potencia = np.random.choice([60, 100, 150, 200, 300, 500, 1000])  # W
    tiempo = np.random.randint(5, 301)  # minutos (entre 5 min y 5h)
    
    # Consumo teórico (kWh)
    consumo = (potencia * tiempo) / (1000 * 60)
    
    # Agregar ruido aleatorio (±5%)
    ruido = np.random.normal(0, 0.05 * consumo)
    consumo_real = max(consumo + ruido, 0)
    
    # Calcular costo
    costo = consumo_real * tarifa
    
    data.append([potencia, tiempo, consumo_real, costo])

df = pd.DataFrame(data, columns=["potencia", "tiempo", "consumo_kwh", "costo_cop"])

# ----------------------------
# Guardar dataset
# ----------------------------
df.to_csv("dataset_consumo.csv", index=False)

print("✅ Dataset generado: dataset_consumo.csv (estrato fijo = 4)")
