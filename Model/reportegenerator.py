import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ----------------------------
# Modelos POO
# ----------------------------
class Usuario:
    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre

class Objeto:
    def __init__(self, id, nombre, potencia_w, consumo_wh):
        self.id = id
        self.nombre = nombre
        self.potencia_w = potencia_w
        self.consumo_wh = consumo_wh

class Reporte:
    def __init__(self, id_usuario, id_objeto, fecha, duracion_minutos, estado, gasto):
        self.id_usuario = id_usuario
        self.id_objeto = id_objeto
        self.fecha = fecha
        self.duracion_minutos = duracion_minutos
        self.estado = estado
        self.gasto = gasto

class ReporteGenerator:
    def __init__(self, usuarios, objetos, tarifa=1000, n_samples=1000):
        self.usuarios = usuarios
        self.objetos = objetos
        self.tarifa = tarifa
        self.n_samples = n_samples
        np.random.seed(42)

    def generar_reportes(self):
        reportes = []
        for _ in range(self.n_samples):
            usuario = np.random.choice(self.usuarios)
            objeto = np.random.choice(self.objetos)
            duracion = np.random.randint(5, 301)  # minutos
            estado = np.random.choice([1, 0])
            fecha = datetime.now() - timedelta(minutes=np.random.randint(0, 10000))
            # Consumo teórico (kWh)
            consumo = (objeto.potencia_w * duracion) / (1000 * 60)
            ruido = np.random.normal(0, 0.05 * consumo)
            consumo_real = max(consumo + ruido, 0)
            gasto = consumo_real * self.tarifa if estado == 1 else 0.0
            reporte = Reporte(
                id_usuario=usuario.id,
                id_objeto=objeto.id,
                fecha=fecha.strftime('%Y-%m-%d %H:%M:%S'),
                duracion_minutos=duracion if estado == 1 else 0.0,
                estado=estado,
                gasto=gasto
            )
            reportes.append(reporte)
        return reportes

    def guardar_csv(self, reportes, filename):
        df = pd.DataFrame([r.__dict__ for r in reportes])
        df.to_csv(filename, index=False)
        print(f"✅ Dataset generado: {filename}")

# ----------------------------
# Datos simulados (como en arduino.sql)
# ----------------------------
usuarios = [
    Usuario(1, 'ADMIN'),
    Usuario(2, 'USER'),
    Usuario(3, 'CHILD'),
]
objetos = [
    Objeto(1, 'LUZ SALA', 60, 0.06),
    Objeto(2, 'LUZ COCINA', 60, 0.06),
    Objeto(3, 'LUZ HABITACIÓN', 60, 0.06),
    Objeto(4, 'LUZ BAÑO', 60, 0.06),
    Objeto(5, 'AIRE ACONDICIONADO', 800, 0.8),
    Objeto(6, 'LAVADORA', 500, 0.5),
    Objeto(7, 'NEVERA', 200, 0.2),
    Objeto(8, 'TELEVISOR', 150, 0.15),
]

if __name__ == "__main__":
    generator = ReporteGenerator(usuarios, objetos, tarifa=1000, n_samples=1000)
    reportes = generator.generar_reportes()
    generator.guardar_csv(reportes, "dataset_reportes.csv")
