def codificar_datos(temperatura, humedad, direccion_viento):
    """
    Codifica los datos meteorológicos en 3 bytes (24 bits)
    Formato: [14 bits temperatura][7 bits humedad][3 bits direccion]
    """
    # Mapeo de direcciones a números
    direcciones = {'N': 0, 'NO': 1, 'O': 2, 'SO': 3, 'S': 4, 'SE': 5, 'E': 6, 'NE': 7}

    # Convertir temperatura a entero (×100 para preservar 2 decimales)
    temp_int = int(temperatura * 100)  # Rango: 0-11000

    # Convertir humedad a entero
    hum_int = humedad  # Rango: 0-100

    # Convertir dirección a número
    dir_int = direcciones[direccion_viento]  # Rango: 0-7

    # Codificar en 24 bits
    datos_24bits = (temp_int << 10) | (hum_int << 3) | dir_int

    # Convertir a 3 bytes
    byte1 = (datos_24bits >> 16) & 0xFF
    byte2 = (datos_24bits >> 8) & 0xFF
    byte3 = datos_24bits & 0xFF

    return bytes([byte1, byte2, byte3])


def decodificar_datos(bytes_3):
    """
    Decodifica 3 bytes a datos meteorológicos
    """
    # Convertir bytes a número de 24 bits
    if len(bytes_3) != 3:
        raise ValueError("Se requieren exactamente 3 bytes")

    datos_24bits = (bytes_3[0] << 16) | (bytes_3[1] << 8) | bytes_3[2]

    # Extraer campos
    dir_int = datos_24bits & 0b111  # Últimos 3 bits
    hum_int = (datos_24bits >> 3) & 0b1111111  # Siguientes 7 bits
    temp_int = (datos_24bits >> 10) & 0b11111111111111  # Primeros 14 bits

    # Mapeo de números a direcciones
    direcciones = ['N', 'NO', 'O', 'SO', 'S', 'SE', 'E', 'NE']

    return {
        "temperatura": round(temp_int / 100.0, 2),
        "humedad": hum_int,
        "direccion_viento": direcciones[dir_int]
    }


# Prueba de codificación/decodificación
if __name__ == "__main__":
    # Datos de prueba
    temp = 25.75
    hum = 65
    viento = "SO"

    print("=== PRUEBA CODIFICACIÓN 3 BYTES ===")
    print(f"Datos originales: Temp={temp}°C, Hum={hum}%, Viento={viento}")

    # Codificar
    bytes_codificados = codificar_datos(temp, hum, viento)
    print(f"Bytes codificados: {bytes_codificados.hex()} ({len(bytes_codificados)} bytes)")

    # Decodificar
    datos_decodificados = decodificar_datos(bytes_codificados)
    print(f"Datos decodificados: Temp={datos_decodificados['temperatura']}°C, "
          f"Hum={datos_decodificados['humedad']}%, Viento={datos_decodificados['direccion_viento']}")

    # Verificar
    assert datos_decodificados["temperatura"] == temp
    assert datos_decodificados["humedad"] == hum
    assert datos_decodificados["direccion_viento"] == viento
    print(" Codificación/decodificación exitosa!")