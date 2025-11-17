import json
import time
import random
from kafka import KafkaProducer
from sensor_simulator import generar_dato_meteorologico
from codificador import codificar_datos  # ← NUEVO

# Configuración de Kafka
KAFKA_SERVER = 'iot.redesuvg.cloud:9092'
TOPIC = '21333'
CLIENT_ID = 'estacion_meteorologica_uvg'


def crear_producer():
    """Crea y configura el Kafka Producer"""
    try:
        producer = KafkaProducer(
            bootstrap_servers=[KAFKA_SERVER],
            client_id=CLIENT_ID,
            # value_serializer=lambda v: json.dumps(v).encode('utf-8'),  # ← QUITAR
            # Ahora enviamos bytes directamente
            acks='all',
            retries=3,
            batch_size=16384,
            linger_ms=10
        )
        print(f"Producer conectado a {KAFKA_SERVER}")
        return producer
    except Exception as e:
        print(f"Error conectando a Kafka: {e}")
        return None


def enviar_datos_meteorologicos(producer, topic):
    """Envía datos meteorológicos codificados en 3 bytes"""
    try:
        # Generar dato meteorológico
        dato = generar_dato_meteorologico()

        # CODIFICAR EN 3 BYTES ← NUEVO
        bytes_codificados = codificar_datos(
            dato['temperatura'],
            dato['humedad'],
            dato['direccion_viento']
        )

        print(f"Datos originales: Temp={dato['temperatura']}°C, "
              f"Hum={dato['humedad']}%, Viento={dato['direccion_viento']}")
        print(f"Bytes codificados: {bytes_codificados.hex()} ({len(bytes_codificados)} bytes)")

        # Enviar bytes codificados (no JSON)
        future = producer.send(
            topic=topic,
            value=bytes_codificados,  # ← Enviamos bytes, no JSON
            key=b'sensor_principal'
        )

        # Esperar confirmación
        metadata = future.get(timeout=10)
        print(f"Dato enviado - Partición: {metadata.partition}, Offset: {metadata.offset}")

        return True

    except Exception as e:
        print(f"Error enviando dato: {e}")
        return False


def main():
    """Función principal del producer"""
    print("=== KAFKA PRODUCER - ESTACIÓN METEOROLÓGICA ===")

    # Crear producer
    producer = crear_producer()
    if not producer:
        return

    contador = 0
    try:
        while True:
            contador += 1
            print(f"\n--- Envío #{contador} ---")

            # Enviar dato
            enviar_datos_meteorologicos(producer, TOPIC)

            # Esperar entre 15 y 30 segundos
            tiempo_espera = random.randint(15, 30)
            print(f"Esperando {tiempo_espera} segundos...")
            time.sleep(tiempo_espera)

    except KeyboardInterrupt:
        print("\n\nProducer detenido por el usuario")
    except Exception as e:
        print(f"\nError inesperado: {e}")
    finally:
        # Cerrar producer
        producer.close()
        print("Producer cerrado correctamente")


if __name__ == "__main__":

    main()
