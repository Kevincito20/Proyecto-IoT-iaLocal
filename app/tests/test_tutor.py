def test_tutor_respuesta_basica(client):
    cuerpo = {
        "mensaje": "Explícame la ley de Ohm",
        "materia": "fisica"
    }

    respuesta = client.post("/api/tutor", json=cuerpo)
    assert respuesta.status_code == 200

    datos = respuesta.json()
    assert "respuesta" in datos
    assert isinstance(datos["respuesta"], str)
    assert len(datos["respuesta"]) > 0

    assert "materia_detectada" in datos
    assert datos["materia_detectada"] == "física"

    assert "es_tarea_sin_contexto" in datos
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
    # Aquí esperamos el mensaje de bloqueo, que no depende de Ollama
    assert "Lo siento, no puedo ayudarte con esa solicitud" in datos["respuesta"]
