from fastapi import APIRouter
import httpx

from app.configuration.ajustes import ajustes


enrutador_sistema = APIRouter(tags=["sistema"])


@enrutador_sistema.get("/salud")
async def obtener_salud():
    """
    Verifica el estado básico del sistema y la conexión con Ollama.
    """
    estado_ollama = "desconocido"

    try:
        async with httpx.AsyncClient(timeout=5.0) as cliente:
            respuesta = await cliente.get(ajustes.url_ollama_tags)
            if respuesta.status_code == 200:
                estado_ollama = "conectado"
            else:
                estado_ollama = f"error_http_{respuesta.status_code}"
    except httpx.RequestError:
        estado_ollama = "no_conectado"

    return {
        "estado": "ok",
        "ollama": estado_ollama,
        "modelo": ajustes.modelo_ollama,
    }
