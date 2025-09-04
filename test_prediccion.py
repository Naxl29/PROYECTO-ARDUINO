# Prueba simple del controlador ML
from Controller.ml_controller import MLController

def main():
    print("=== Prueba Simple ML con Datos Reales (Pesos Colombianos) ===")
    
    ml_controller = MLController()
    
    # Entrenar modelo
    print("1. Entrenando modelo...")
    resultado = ml_controller.entrenar_modelo()
    print(f"   {resultado['mensaje']}")
    
    # Predicción automática
    if resultado['exitoso']:
        print("2. Predicción con promedio automático:")
        prediccion = ml_controller.predecir_recibo()
        if prediccion['exitoso']:
            print(f"   Costo: ${prediccion['prediccion']:,.0f} COP para {prediccion['consumo']:.3f} kWh")
        
        # Predicción específica
        print("3. Predicción con 0.5 kWh:")
        prediccion = ml_controller.predecir_recibo(0.5)
        if prediccion['exitoso']:
            print(f"   Costo: ${prediccion['prediccion']:,.0f} COP")

if __name__ == "__main__":
    main()
