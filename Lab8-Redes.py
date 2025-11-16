import random
from datetime import datetime

# Configuración inicial
random.seed(42)  # Para resultados reproducibles


def generar_temperatura():
    """Genera temperatura con distribución normal centrada en 25°C"""
    media = 25.0
    desviacion = 10.0
    temp = random.gauss(media, desviacion)

    # Asegurar que esté en el rango [0, 110.00]
    temp = max(0, min(temp, 110.0))
    return round(temp, 2)


def generar_humedad():
    """Genera humedad con distribución normal centrada en 60%"""
    media = 60
    desviacion = 20
    humedad = random.gauss(media, desviacion)

    # Asegurar que esté en el rango [0, 100]
    humedad = int(max(0, min(humedad, 100)))
    return humedad


def generar_direccion_viento():
    """Genera dirección del viento aleatoria"""
    direcciones = ['N', 'NO', 'O', 'SO', 'S', 'SE', 'E', 'NE']
    return random.choice(direcciones)


def generar_dato_meteorologico():
    """Genera un dato meteorológico completo"""
    return {
        "temperatura": generar_temperatura(),
        "humedad": generar_humedad(),
        "direccion_viento": generar_direccion_viento(),
        "timestamp": datetime.now().isoformat()
    }


# Prueba de generación de datos
if __name__ == "__main__":
    print("=== SIMULADOR DE ESTACIÓN METEOROLÓGICA ===")
    print("Generando 10 mediciones de prueba:\n")

    for i in range(10):
        dato = generar_dato_meteorologico()
        print(f"Medición {i + 1}:")
        print(f"  Temperatura: {dato['temperatura']}°C")
        print(f"  Humedad: {dato['humedad']}%")
        print(f"  Dirección viento: {dato['direccion_viento']}")
        print(f"  Timestamp: {dato['timestamp']}")
        print("-" * 40)