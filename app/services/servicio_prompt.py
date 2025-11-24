from typing import Optional, List

from app.core.config import settings
from app.models.modelos_tutor import Mensaje


# Límite duro de caracteres por mensaje de historial para el prompt
MAX_CARACTERES_MENSAJE_HISTORIAL = 200


def construir_prompt_pedagogico(
    mensaje_usuario: str,
    materia_norm: Optional[str],
    es_tarea_sin_contexto: bool,
    mensajes_anteriores: Optional[List[Mensaje]] = None,
) -> str:
    """
    Construye un prompt pensado para el modelo phi3:mini,
    orientado a educación y explicación paso a paso.

    Optimizaciones:
    - Usa solo los últimos N mensajes de historial (configurable).
    - Recorta cada mensaje de historial a un máximo de caracteres.
    - Indica al modelo si ya hay conversación en curso para evitar
      saludos repetitivos.
    """

    partes_prompt: list[str] = []

    partes_prompt.append(
        "Actúas como un tutor pedagógico paciente y claro para estudiantes de nivel escolar. "
        "Explicas los temas paso a paso, usando ejemplos sencillos cuando sea útil. "
        "Evitas dar solo la respuesta final: ayudas al estudiante a comprender el proceso."
    )

    if mensajes_anteriores:
        partes_prompt.append(
            "Ya tienes una conversación en curso con este estudiante. "
            "No vuelvas a presentarte ni a decir 'bienvenido' o saludos largos. "
            "Simplemente continúa la explicación de forma natural, "
            "como si fuera un diálogo en progreso."
        )
    else:
        partes_prompt.append(
            "Esta es la primera interacción con el estudiante en esta conversación. "
            "Puedes saludar brevemente, pero evita textos de bienvenida muy largos."
        )

    if materia_norm:
        partes_prompt.append(
            f"La materia principal de esta pregunta es: {materia_norm}."
        )

    if es_tarea_sin_contexto:
        partes_prompt.append(
            "La solicitud del estudiante parece ser una tarea sin mucho contexto. "
            "En lugar de resolverla directamente, guía al estudiante paso a paso, "
            "haciendo preguntas intermedias si es necesario."
        )

    # Incluir un pequeño resumen del contexto anterior (solo los últimos N mensajes)
    if mensajes_anteriores:
        max_mensajes = max(1, settings.max_mensajes_historial)
        partes_prompt.append("Contexto reciente de la conversación:")
        for mensaje in mensajes_anteriores[-max_mensajes:]:
            rol = mensaje.rol.upper()
            contenido = mensaje.contenido.strip()
            if len(contenido) > MAX_CARACTERES_MENSAJE_HISTORIAL:
                contenido = contenido[:MAX_CARACTERES_MENSAJE_HISTORIAL] + "…"
            partes_prompt.append(f"{rol}: {contenido}")

    partes_prompt.append(
        f"Último mensaje del estudiante:\n\"{mensaje_usuario}\"\n"
    )

    partes_prompt.append(
        "Responde ahora de forma clara, organizada y pedagógica en español."
    )

    return "\n\n".join(partes_prompt)
