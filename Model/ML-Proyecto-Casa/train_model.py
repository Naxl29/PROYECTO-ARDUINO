import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

# ----------------------------
# 1. Cargar dataset realista
# ----------------------------
df = pd.read_csv("dataset_consumo.csv")

print("Ejemplo de dataset cargado:")
print(df.head())

# ----------------------------
# 2. Definir variables
# ----------------------------
X = df[["potencia", "tiempo"]]  # solo potencia y tiempo
y = df["consumo_kwh"]

# ----------------------------
# 3. Entrenar modelo
# ----------------------------
modelo = LinearRegression(fit_intercept=False)
modelo.fit(X, y)

# ----------------------------
# 4. Guardar modelo entrenado
# ----------------------------
joblib.dump(modelo, "modelo.pkl")

print("✅ Modelo entrenado y guardado como modelo.pkl (estrato fijo = 4)")
