from fastapi import APIRouter

from app.models.modelos_tutor import SolicitudTutor, RespuestaTutor
from app.services.servicio_tutor import tutor, obtener_materia_normalizada, es_tarea_sin_contexto

enrutador = APIRouter(prefix="/tutor", tags=["tutor"])


@enrutador.post("", response_model=RespuestaTutor)
async def invocar_tutor(solicitud: SolicitudTutor) -> RespuestaTutor:
    """
    Endpoint principal del tutor educativo local.
    """
    respuesta_texto = await tutor(solicitud.mensaje, solicitud.materia)

    materia_detectada = obtener_materia_normalizada(solicitud.materia)
    tarea_flag = es_tarea_sin_contexto(solicitud.mensaje)

    return RespuestaTutor(
        respuesta=respuesta_texto,
        materia_detectada=materia_detectada,
        es_tarea_sin_contexto=tarea_flag,
    )
