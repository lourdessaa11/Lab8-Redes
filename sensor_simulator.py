import time
import matplotlib.pyplot as plt
from tabulate import tabulate


# PROBLEMA 1
def function_problema1(n):
    """
    Implementación del problema 1
    Complejidad: O(n² log n)
    """
    counter = 0
    for i in range(n // 2, n + 1):
        for j in range(1, n // 2 + 1):
            k = 1
            while k <= n:
                counter += 1
                k = k * 2
    return counter


# PROBLEMA 2
def function_problema2(n):
    """
    Implementación del problema 2
    Complejidad: O(n) - debido al break
    """
    if n <= 1:
        return

    for i in range(1, n + 1):
        for j in range(1, n + 1):
            # En lugar de printf, usamos pass
            pass
            break  # El break hace que el loop interno solo ejecute 1 vez


# PROBLEMA 3
def function_problema3(n):
    """
    Implementación del problema 3
    Complejidad: O(n²)
    """
    for i in range(1, n // 3 + 1):
        j = 1
        while j <= n:
            # En lugar de printf, usamos pass
            pass
            j += 4


# PROFILING
def profile_function(func, test_values, nombre_problema):
    """
    Realiza profiling de una función con diferentes valores de n
    """

    print(f"\nProfiling: {nombre_problema}")

    resultados = []

    for idx, n in enumerate(test_values, 1):
        print(f"Probando n = {n:>7}... ", end='', flush=True)

        # Medición de tiempo
        start_time = time.perf_counter()
        func(n)
        end_time = time.perf_counter()

        execution_time = (end_time - start_time) * 1000  # Convertir a milisegundos
        resultados.append([n, f"{execution_time:.6f}"])

        # Mostrar tiempo en formato legible
        if execution_time < 1000:
            print(f"✓ {execution_time:.3f} ms")
        else:
            print(f"✓ {execution_time / 1000:.3f} segundos")

    return resultados


# VISUALIZACIÓN
def crear_tabla_y_grafica(resultados, nombre_problema, complejidad_teorica):
    """
    Crea tabla formateada y gráfica de los resultados
    """
    # Crear tabla
    headers = ["n (tamaño input)", "Tiempo (ms)"]
    print(f"\n{nombre_problema}")
    print(f"Complejidad teórica: {complejidad_teorica}")
    print(tabulate(resultados, headers=headers, tablefmt="grid"))

    # Preparar datos para gráfica
    n_values = [r[0] for r in resultados]
    times = [float(r[1]) for r in resultados]

    return n_values, times


def plot_all_results(all_results):
    """
    Crea gráficas para todos los problemas
    """
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    fig.suptitle('Análisis de Complejidad Temporal - Laboratorio 8', fontsize=16, fontweight='bold')

    problemas = [
        ("Problema 1", "O(n² log n)"),
        ("Problema 2", "O(n)"),
        ("Problema 3", "O(n²)")
    ]

    for idx, (ax, (nombre, complejidad)) in enumerate(zip(axes, problemas)):
        n_values, times = all_results[idx]

        ax.plot(n_values, times, 'o-', linewidth=2, markersize=8, label='Tiempo medido')
        ax.set_xlabel('Tamaño de entrada (n)', fontsize=11, fontweight='bold')
        ax.set_ylabel('Tiempo de ejecución (ms)', fontsize=11, fontweight='bold')
        ax.set_title(f'{nombre}\nComplejidad: {complejidad}', fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend()

        # Escala logarítmica para mejor visualización
        if max(times) / min([t for t in times if t > 0] or [1]) > 100:
            ax.set_yscale('log')
            ax.set_ylabel('Tiempo de ejecución (ms) - escala log', fontsize=11, fontweight='bold')

    plt.tight_layout()
    plt.show()


# ============= EJECUCIÓN PRINCIPAL =============
def main():
    # Valores de prueba
    test_values = [1, 10, 100, 1000, 10000]
    #test_values = [1, 10, 100, 1000, 10000, 100000]
    #test_values = [1, 10, 100, 1000, 10000, 100000, 1000000]

    # Tiempo total de ejecución
    total_start = time.perf_counter()

    print("\nLab 8")

    all_results = []

    # Problema 1
    resultados1 = profile_function(function_problema1, test_values, "Problema 1")
    n_vals1, times1 = crear_tabla_y_grafica(resultados1, "\nTabla Problema 1", "O(n² log n)")
    all_results.append((n_vals1, times1))

    # Problema 2
    resultados2 = profile_function(function_problema2, test_values, "Problema 2")
    n_vals2, times2 = crear_tabla_y_grafica(resultados2, "\nTabla Problema 2", "O(n)")
    all_results.append((n_vals2, times2))

    # Problema 3
    resultados3 = profile_function(function_problema3, test_values, "Problema 3")
    n_vals3, times3 = crear_tabla_y_grafica(resultados3, "\nTabla Problema 3", "O(n²)")
    all_results.append((n_vals3, times3))

    # Crear gráficas
    print("\nGráficas")
    plot_all_results(all_results)

    # Tiempo total
    total_end = time.perf_counter()
    total_time = total_end - total_start

    print(f"\nTiempo Total: {total_time:.3f} segundos ({total_time / 60:.2f} minutos)")

if __name__ == "__main__":
    main()