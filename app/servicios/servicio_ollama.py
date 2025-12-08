import asyncio
import json
from typing import AsyncGenerator

import httpx

from app.configuracion.ajustes import ajustes


_cliente_http: httpx.AsyncClient | None = None
_semaforo_ollama = asyncio.Semaphore(1)


def obtener_cliente_http() -> httpx.AsyncClient:
    """
    Crea o devuelve un cliente HTTP reutilizable para comunicarse con Ollama.
    """
    global _cliente_http
    if _cliente_http is None:
        _cliente_http = httpx.AsyncClient(timeout=120.0)
    return _cliente_http


async def generar_stream_respuesta(prompt_completo: str) -> AsyncGenerator[str, None]:
    """
    Envía el prompt a Ollama y genera fragmentos de texto en streaming.
    Cada elemento generado es un fragmento de texto ya listo para enviar al cliente.
    Se limita la concurrencia mediante un semáforo para no saturar el modelo.
    """
    cliente = obtener_cliente_http()

    cuerpo_peticion = {
        "model": ajustes.modelo_ollama,
        "prompt": prompt_completo,
        "stream": True,
        "options": {
            "temperature": ajustes.temperatura_por_defecto,
            "num_predict": ajustes.maximo_tokens,
        },
    }

    async with _semaforo_ollama:
        try:
            async with cliente.stream(
                "POST",
                ajustes.url_ollama_generar,
                json=cuerpo_peticion,
            ) as respuesta:
                async for linea in respuesta.aiter_lines():
                    if not linea:
                        continue

                    try:
                        datos = json.loads(linea)
                    except json.JSONDecodeError:
                        continue

                    if "error" in datos:
                        mensaje_error = datos.get("error", "Error desconocido en Ollama")
                        yield f"[Error Ollama] {mensaje_error}"
                        return

                    fragmento = datos.get("response", "")
                    if fragmento:
                        yield fragmento

                    if datos.get("done"):
                        break

        except httpx.RequestError as error:
            yield f"No se pudo conectar a Ollama: {error}"
