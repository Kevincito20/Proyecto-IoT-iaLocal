import asyncio


async def generar_respuesta_ia(prompt: str) -> str:
    """
    FASE 2:
    Simula la respuesta de un modelo de IA.
    En FASE 3 este código se reemplazará por la llamada real a Ollama (phi3:mini).
    """
    # Pequeño retraso artificial para simular trabajo de IA (muy corto).
    await asyncio.sleep(0.01)

    return (
        "Esta es una respuesta simulada del tutor educativo.\n\n"
        "Más adelante, esta parte del sistema usará el modelo local phi3:mini en Ollama.\n\n"
        f"Prompt recibido:\n{prompt}"
    )
