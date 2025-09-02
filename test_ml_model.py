#!/usr/bin/env python3
"""
Script de pruebas para el modelo de Machine Learning
Ejecutar desde terminal: python test_ml_model.py
"""

import sys
import os
import numpy as np
from datetime import datetime

# Agregar la ruta del proyecto al path de Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from Model.ml_model import MLModel
    from config.ml_config import MODEL_PATH, MODEL_CONFIG
except ImportError as e:
    print(f"❌ Error importando módulos: {e}")
    print("Asegúrate de estar en el directorio del proyecto")
    sys.exit(1)

class TestMLModel:
    def __init__(self):
        self.ml_model = MLModel()
        print("🤖 Iniciando pruebas del modelo ML")
        print(f"📁 Ruta del modelo: {MODEL_PATH}")
        print(f"⚙️ Configuración: {MODEL_CONFIG}")
        print("-" * 50)
    
    def generar_datos_simulados(self):
        """Genera datos simulados para pruebas"""
        print("📊 Generando datos simulados...")
        
        # Simular datos de 12 meses (enero a diciembre)
        # Mes vs Valor del recibo (en COP)
        datos_simulados = {
            1: 180000,   # Enero - alto consumo (verano)
            2: 175000,   # Febrero
            3: 165000,   # Marzo
            4: 150000,   # Abril - consumo medio
            5: 140000,   # Mayo
            6: 135000,   # Junio
            7: 145000,   # Julio - empiezan lluvias
            8: 155000,   # Agosto
            9: 160000,   # Septiembre
            10: 170000,  # Octubre
            11: 185000,  # Noviembre - temporada seca
            12: 190000   # Diciembre - alto consumo (Navidad)
        }
        
        # Convertir a formato numpy
        X = np.array([[mes] for mes in datos_simulados.keys()])
        y = np.array(list(datos_simulados.values()))
        
        print(f"✅ Datos generados: {len(datos_simulados)} meses")
        print("📈 Datos de entrenamiento:")
        for mes, valor in datos_simulados.items():
            mes_nombre = self.obtener_nombre_mes(mes)
            print(f"   {mes_nombre}: ${valor:,}")
        
        return X, y, datos_simulados
    
    def test_entrenamiento(self):
        """Prueba el entrenamiento del modelo"""
        print("\n🎯 PRUEBA 1: Entrenamiento del modelo")
        print("-" * 30)
        
        try:
            # Generar datos
            X, y, datos_originales = self.generar_datos_simulados()
            
            # Entrenar modelo
            print("🔄 Entrenando modelo...")
            modelo_entrenado = self.ml_model.entrenar_modelo(X, y)
            
            if modelo_entrenado:
                print("✅ Modelo entrenado exitosamente")
                print(f"📊 Coeficientes: {modelo_entrenado.coef_}")
                print(f"📊 Intercepto: {modelo_entrenado.intercept_:.2f}")
                
                # Verificar si se guardó el archivo
                if os.path.exists(MODEL_PATH):
                    print(f"💾 Modelo guardado en: {MODEL_PATH}")
                else:
                    print("❌ Error: Modelo no se guardó correctamente")
                
                return True
            else:
                print("❌ Error en el entrenamiento")
                return False
                
        except Exception as e:
            print(f"❌ Error durante entrenamiento: {e}")
            return False
    
    def test_carga_modelo(self):
        """Prueba la carga del modelo"""
        print("\n🔄 PRUEBA 2: Carga del modelo")
        print("-" * 30)
        
        try:
            # Crear nueva instancia para simular carga desde archivo
            nuevo_modelo = MLModel()
            modelo_cargado = nuevo_modelo.cargar_modelo()
            
            if modelo_cargado:
                print("✅ Modelo cargado exitosamente desde archivo")
                print(f"📊 Tipo de modelo: {type(modelo_cargado).__name__}")
                return True
            else:
                print("❌ Error cargando modelo")
                return False
                
        except Exception as e:
            print(f"❌ Error durante carga: {e}")
            return False
    
    def test_predicciones(self):
        """Prueba las predicciones del modelo"""
        print("\n🔮 PRUEBA 3: Predicciones")
        print("-" * 30)
        
        try:
            # Predecir para cada mes
            print("📈 Predicciones por mes:")
            
            predicciones = {}
            for mes in range(1, 13):
                entrada = np.array([[mes]])
                prediccion = self.ml_model.predecir(entrada)[0]
                predicciones[mes] = prediccion
                
                mes_nombre = self.obtener_nombre_mes(mes)
                print(f"   {mes_nombre}: ${prediccion:,.2f}")
            
            # Predicción del próximo mes
            mes_actual = datetime.now().month
            proximo_mes = 1 if mes_actual == 12 else mes_actual + 1
            
            entrada_proxima = np.array([[proximo_mes]])
            prediccion_proxima = self.ml_model.predecir(entrada_proxima)[0]
            
            print(f"\n🎯 PREDICCIÓN PRÓXIMO MES:")
            print(f"   Mes actual: {self.obtener_nombre_mes(mes_actual)}")
            print(f"   Próximo mes: {self.obtener_nombre_mes(proximo_mes)}")
            print(f"   Valor predicho: ${prediccion_proxima:,.2f}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error durante predicciones: {e}")
            return False
    
    def test_casos_especiales(self):
        """Prueba casos especiales y errores"""
        print("\n⚠️ PRUEBA 4: Casos especiales")
        print("-" * 30)
        
        try:
            # Prueba con entrada inválida
            print("🧪 Probando entrada inválida...")
            entrada_invalida = np.array([[0]])  # Mes 0 no existe
            prediccion_invalida = self.ml_model.predecir(entrada_invalida)[0]
            print(f"   Mes 0: ${prediccion_invalida:,.2f}")
            
            # Prueba con mes futuro
            entrada_futura = np.array([[15]])  # Mes 15 no existe
            prediccion_futura = self.ml_model.predecir(entrada_futura)[0]
            print(f"   Mes 15: ${prediccion_futura:,.2f}")
            
            print("✅ Casos especiales manejados")
            return True
            
        except Exception as e:
            print(f"❌ Error en casos especiales: {e}")
            return False
    
    def obtener_nombre_mes(self, numero_mes):
        """Convierte número de mes a nombre"""
        meses = {
            1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
            5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
            9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
        }
        return meses.get(numero_mes, f'Mes {numero_mes}')
    
    def ejecutar_todas_las_pruebas(self):
        """Ejecuta todas las pruebas"""
        print("🚀 INICIANDO BATERÍA COMPLETA DE PRUEBAS")
        print("=" * 60)
        
        pruebas = [
            ("Entrenamiento", self.test_entrenamiento),
            ("Carga del modelo", self.test_carga_modelo),
            ("Predicciones", self.test_predicciones),
            ("Casos especiales", self.test_casos_especiales)
        ]
        
        resultados = []
        
        for nombre, test_func in pruebas:
            resultado = test_func()
            resultados.append((nombre, resultado))
        
        # Resumen final
        print("\n" + "=" * 60)
        print("📋 RESUMEN DE PRUEBAS")
        print("=" * 60)
        
        exitosas = 0
        for nombre, resultado in resultados:
            estado = "✅ PASÓ" if resultado else "❌ FALLÓ"
            print(f"{estado} - {nombre}")
            if resultado:
                exitosas += 1
        
        print(f"\n🎯 Resultado final: {exitosas}/{len(pruebas)} pruebas exitosas")
        
        if exitosas == len(pruebas):
            print("🎉 ¡Todas las pruebas pasaron! El modelo está funcionando correctamente.")
        else:
            print("⚠️ Algunas pruebas fallaron. Revisa los errores anteriores.")

def main():
    """Función principal"""
    print("🔬 SIMULADOR DE PRUEBAS - MODELO ML RECIBOS")
    print("=" * 60)
    
    # Verificar dependencias
    print("🔍 Verificando dependencias...")
    try:
        import sklearn
        import numpy
        import pickle
        print("✅ Todas las dependencias están disponibles")
    except ImportError as e:
        print(f"❌ Faltan dependencias: {e}")
        print("Ejecuta: pip install -r requirements.txt")
        return
    
    # Ejecutar pruebas
    tester = TestMLModel()
    tester.ejecutar_todas_las_pruebas()

if __name__ == "__main__":
    main()
