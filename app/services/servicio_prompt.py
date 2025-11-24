from typing import Optional


def construir_prompt_pedagogico(
    mensaje_usuario: str,
    materia_norm: Optional[str],
    es_tarea_sin_contexto: bool,
) -> str:
    """
    Construye un prompt pensado para el modelo phi3:mini,
    orientado a educación y explicación paso a paso.
    """

    partes_prompt: list[str] = []

    partes_prompt.append(
        "Actúa como un tutor pedagógico paciente y claro para estudiantes de nivel escolar. "
        "Explica los temas paso a paso, usando ejemplos sencillos cuando sea útil. "
        "Evita dar solo la respuesta final: ayuda al estudiante a comprender el proceso."
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

    partes_prompt.append(
        f"Pregunta del estudiante:\n\"{mensaje_usuario}\"\n"
    )

    partes_prompt.append(
        "Ahora responde de forma clara, organizada y pedagógica en español."
    )

    return "\n\n".join(partes_prompt)
