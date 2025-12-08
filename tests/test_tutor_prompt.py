from app.service.servicio_tutor import construir_prompt_tutor


def test_prompt_tutor_no_promueve_frases_de_relleno_al_inicio():
    """
    Verifica que el prompt del tutor indique no usar frases de relleno
    y que no proponga comenzar con 'Entiendo que'.
    """
    conversacion = "Estudiante: ¿Qué es la química?"
    prompt = construir_prompt_tutor(conversacion)

    assert "No uses frases de relleno al inicio como 'Entiendo que'" in prompt
    assert "Entiendo que te gustaría" not in prompt
