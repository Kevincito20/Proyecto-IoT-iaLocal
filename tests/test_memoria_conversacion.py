import os

import psutil

from app.service import servicio_conversacion as sc


def obtener_memoria_mb() -> float:
    """
    Devuelve la memoria residente del proceso actual en megabytes.
    """
    proceso = psutil.Process(os.getpid())
    return proceso.memory_info().rss / (1024 * 1024)


def test_consumo_memoria_conversacion_limitado():
    """
    Agrega un número razonable de mensajes y verifica que el consumo de memoria
    del proceso no aumente por encima de un límite amplio.
    El valor del límite es orientativo y puede ajustarse según el entorno.
    """
    memoria_inicial = obtener_memoria_mb()

    sc.reiniciar_conversacion()

    for _ in range(2000):
        sc.agregar_mensaje("usuario", "mensaje de prueba " * 10)

    resumen = sc.obtener_resumen_conversaciones()
    assert len(resumen) >= 1

    memoria_final = obtener_memoria_mb()
    incremento = memoria_final - memoria_inicial

    assert incremento < 100.0, f"El incremento de memoria fue demasiado alto: {incremento:.2f} MB"
