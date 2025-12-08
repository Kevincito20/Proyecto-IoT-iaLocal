def extraer_mensaje_actual(texto_conversacion: str) -> str:
    """
    Extrae el mensaje actual del estudiante desde el texto de conversación
    enviado por el cliente. Si no encuentra el marcador esperado,
    devuelve el texto original.

    Formato esperado al final del texto:
    'Mensaje actual del estudiante: "..."'
    """
    marcador = "Mensaje actual del estudiante:"
    posicion = texto_conversacion.rfind(marcador)
    if posicion == -1:
        return texto_conversacion.strip()

    segmento = texto_conversacion[posicion + len(marcador):].strip()
    if segmento.startswith('"') and segmento.endswith('"'):
        return segmento[1:-1].strip()

    return segmento
