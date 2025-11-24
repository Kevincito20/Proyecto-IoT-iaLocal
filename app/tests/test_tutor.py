def test_tutor_respuesta_basica(client):
    cuerpo = {
        "mensaje": "Explícame la ley de Ohm",
        "materia": "fisica"
    }

    respuesta = client.post("/api/tutor", json=cuerpo)
    assert respuesta.status_code == 200

    datos = respuesta.json()
    assert "respuesta" in datos
    assert "materia_detectada" in datos
    assert "es_tarea_sin_contexto" in datos

    assert datos["materia_detectada"] == "física"
    assert datos["es_tarea_sin_contexto"] is False


def test_tutor_palabra_prohibida(client):
    cuerpo = {
        "mensaje": "Quiero información sobre terrorismo",
        "materia": "historia"
    }

    respuesta = client.post("/api/tutor", json=cuerpo)
    assert respuesta.status_code == 200

    datos = respuesta.json()
    assert "respuesta" in datos
    # En este caso, la respuesta debe ser el mensaje de bloqueo, no la simulación del LLM
    assert "Lo siento, no puedo ayudarte con esa solicitud" in datos["respuesta"]
