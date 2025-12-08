from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.modelos.chat import PeticionChat
from app.servicios.servicio_tutor import construir_prompt_tutor
from app.servicios.servicio_ollama import generar_stream_respuesta
from app.servicios.servicio_conversacion import (
    agregar_mensaje,
    reiniciar_conversacion,
)
from app.utilidades.util_texto import extraer_mensaje_actual


enrutador_chat = APIRouter(tags=["chat"])


@enrutador_chat.post("/chat/stream")
async def chat_stream(peticion: PeticionChat) -> StreamingResponse:
    """
    Recibe el mensaje del cliente, registra el mensaje actual del usuario,
    construye el prompt del tutor y devuelve la respuesta en streaming.
    Al finalizar, registra también la respuesta completa del tutor.
    """

    mensaje_actual = extraer_mensaje_actual(peticion.mensaje)
    if mensaje_actual:
        agregar_mensaje("usuario", mensaje_actual)

    prompt_completo = construir_prompt_tutor(peticion.mensaje)

    async def generador_eventos():
        respuesta_completa = ""

        async for fragmento in generar_stream_respuesta(prompt_completo):
            respuesta_completa += fragmento
            texto_limpio = fragmento.replace("\n", " ")
            yield f"data: {texto_limpio}\n\n"

        respuesta_final = respuesta_completa.strip()
        if respuesta_final:
            agregar_mensaje("tutor", respuesta_final)

    return StreamingResponse(
        generador_eventos(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )


@enrutador_chat.post("/chat/reiniciar")
async def chat_reiniciar():
    """
    Reinicia la conversación almacenada en memoria.
    """
    reiniciar_conversacion()
    return {"estado": "reiniciado"}
