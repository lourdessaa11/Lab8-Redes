import json
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from kafka import KafkaConsumer
from collections import deque
from datetime import datetime
from codificador import decodificar_datos

# Configuración
KAFKA_SERVER = 'iot.redesuvg.cloud:9092'
TOPIC = '21333'
GROUP_ID = 'grupo_visualizacion'

# Listas para almacenar datos
MAX_POINTS = 50
temperaturas = deque(maxlen=MAX_POINTS)
humedades = deque(maxlen=MAX_POINTS)
vientos = {'N': 0, 'NO': 0, 'O': 0, 'SO': 0, 'S': 0, 'SE': 0, 'E': 0, 'NE': 0}
timestamps = deque(maxlen=MAX_POINTS)

# Crear consumer
consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=[KAFKA_SERVER],
    group_id=GROUP_ID,
    # value_deserializer=lambda m: json.loads(m.decode('utf-8')),  # ← QUITAR
    # Ahora recibimos bytes directamente
    auto_offset_reset='latest',
    enable_auto_commit=True
)

print(f"Consumer conectado. Esperando mensajes del topic '{TOPIC}'...")

# Configurar la figura
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 10))
fig.suptitle('Estación Meteorológica - Datos en Tiempo Real (3 BYTES)', fontsize=16)


def procesar_mensaje():
    """Lee y decodifica mensajes de Kafka"""
    try:
        msg_pack = consumer.poll(timeout_ms=100)

        for tp, messages in msg_pack.items():
            for message in messages:
                # DECODIFICAR BYTES A DATOS ← NUEVO
                bytes_recibidos = message.value
                dato = decodificar_datos(bytes_recibidos)

                print(f"Bytes recibidos: {bytes_recibidos.hex()} ({len(bytes_recibidos)} bytes)")
                print(f"Dato decodificado - Temp: {dato['temperatura']}°C, "
                      f"Humedad: {dato['humedad']}%, Viento: {dato['direccion_viento']}")

                # Agregar datos a las listas
                temperaturas.append(dato['temperatura'])
                humedades.append(dato['humedad'])
                vientos[dato['direccion_viento']] += 1
                timestamps.append(datetime.now())

    except Exception as e:
        print(f"Error procesando mensaje: {e}")


def actualizar_graficos(frame):
    """Actualiza los gráficos con los nuevos datos"""
    # Procesar nuevos mensajes
    procesar_mensaje()

    # Limpiar los ejes
    ax1.clear()
    ax2.clear()
    ax3.clear()

    # Gráfico 1: Temperatura
    if len(temperaturas) > 0:
        ax1.plot(range(len(temperaturas)), list(temperaturas),
                 'r-o', linewidth=2, markersize=4)
        ax1.set_ylabel('Temperatura (°C)', fontsize=12)
        ax1.set_title('Temperatura')
        ax1.grid(True, alpha=0.3)
        ax1.set_ylim(0, 110)

    # Gráfico 2: Humedad
    if len(humedades) > 0:
        ax2.plot(range(len(humedades)), list(humedades),
                 'b-o', linewidth=2, markersize=4)
        ax2.set_ylabel('Humedad (%)', fontsize=12)
        ax2.set_title('Humedad Relativa')
        ax2.grid(True, alpha=0.3)
        ax2.set_ylim(0, 100)

    # Gráfico 3: Dirección del viento (barras)
    direcciones = list(vientos.keys())
    conteos = list(vientos.values())
    ax3.bar(direcciones, conteos, color='green', alpha=0.7)
    ax3.set_ylabel('Frecuencia', fontsize=12)
    ax3.set_xlabel('Dirección', fontsize=12)
    ax3.set_title('Distribución de Dirección del Viento')
    ax3.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()


# Crear animación que se actualiza cada segundo
ani = FuncAnimation(fig, actualizar_graficos, interval=1000, cache_frame_data=False)

try:
    plt.show()
except KeyboardInterrupt:
    print("\n\nConsumer detenido por el usuario")
finally:
    consumer.close()
    print("Consumer cerrado correctamente")