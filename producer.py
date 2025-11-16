import json
import time
import random
from kafka import KafkaProducer
from sensor_simulator import generar_dato_meteorologico

# Configuración de Kafka
KAFKA_SERVER = 'iot.redesuvg.cloud:9092'
TOPIC = '21333'  # Número de carné
CLIENT_ID = 'estacion_meteorologica_uvg'


def crear_producer():
    """Crea y configura el Kafka Producer"""
    try:
        producer = KafkaProducer(
            bootstrap_servers=[KAFKA_SERVER],
            client_id=CLIENT_ID,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            # Configuraciones adicionales para mejor rendimiento
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
    """Envía datos meteorológicos al topic de Kafka"""
    try:
        # Generar dato meteorológico
        dato = generar_dato_meteorologico()

        # Enviar al topic de Kafka
        future = producer.send(
            topic=topic,
            value=dato,
            key=b'sensor_principal'  # Misma key para misma partición
        )

        # Opcional: esperar confirmación
        metadata = future.get(timeout=10)

        print(f"Dato enviado - Partición: {metadata.partition}, Offset: {metadata.offset}")
        print(
            f"   Temperatura: {dato['temperatura']}°C, Humedad: {dato['humedad']}%, Viento: {dato['direccion_viento']}")

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
