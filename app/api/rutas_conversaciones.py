from fastapi import APIRouter, HTTPException

from app.service.servicio_conversacion import (
    obtener_resumen_conversaciones_completo,
    obtener_conversacion_por_id,
    establecer_conversacion_actual,
)

enrutador_conversaciones = APIRouter(tags=["conversaciones"])


@enrutador_conversaciones.get("/conversaciones/resumen")
async def obtener_resumen_conversaciones():
    """
    Devuelve el listado de conversaciones existentes (máximo 3)
    y cuál es la conversación actual.
    """
    return obtener_resumen_conversaciones_completo()


@enrutador_conversaciones.get("/conversaciones/{id_conversacion}")
async def obtener_conversacion(id_conversacion: int):
    """
    Devuelve todos los mensajes de una conversación específica.
    """
    conversacion = obtener_conversacion_por_id(id_conversacion)
    if conversacion is None:
        raise HTTPException(status_code=404, detail="Conversación no encontrada")

    mensajes = [
        {
            "rol": mensaje.rol,
            "contenido": mensaje.contenido,
            "marca_tiempo": mensaje.marca_tiempo.isoformat(),
        }
        for mensaje in conversacion.mensajes
    ]

    return {
        "id_conversacion": conversacion.id_conversacion,
        "fecha_inicio": conversacion.fecha_inicio.isoformat(),
        "mensajes": mensajes,
    }


@enrutador_conversaciones.post("/conversaciones/{id_conversacion}/activar")
async def activar_conversacion(id_conversacion: int):
    """
    Establece una conversación como la conversación actual.
    """
    exito = establecer_conversacion_actual(id_conversacion)
    if not exito:
        raise HTTPException(status_code=404, detail="Conversación no encontrada")

    return {"estado": "ok", "id_conversacion": id_conversacion}
