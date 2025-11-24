import asyncio
import logging
from time import perf_counter

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)

# Semáforo para limitar cuántas peticiones simultáneas se hacen al modelo
# En Raspberry Pi, lo ideal es 1 para no saturar la RAM/CPU.
_semaforo_llm = asyncio.Semaphore(max(1, settings.max_concurrencia_llm))


async def generar_respuesta_ia(prompt: str) -> str:
    """
    Genera una respuesta usando el modelo local de Ollama (phi3:mini por defecto).

    Optimizaciones:
    - Sin streaming.
    - Tokens de salida limitados (MAX_TOKENS_RESPUESTA).
    - Timeout configurable.
    - Concurrencia limitada mediante un semáforo.
    - Métricas básicas de tiempo y tamaño de prompt (en modo debug).
    """

    url = f"{settings.ollama_host}/api/generate"

    cuerpo = {
        "model": settings.ollama_modelo,
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_predict": settings.max_tokens_respuesta,
            "temperature": settings.temperatura_modelo,
        },
    }

    inicio = perf_counter()
    async with _semaforo_llm:
        try:
            async with httpx.AsyncClient(
                timeout=settings.ollama_timeout_segundos
            ) as cliente:
                respuesta = await cliente.post(url, json=cuerpo)

            respuesta.raise_for_status()
            datos = respuesta.json()

            texto = datos.get("response", "").strip()
            if not texto:
                return (
                    "Lo siento, no pude generar una respuesta en este momento. "
                    "Por favor, intenta nuevamente más tarde."
                )

            return texto

        except httpx.RequestError as exc:
            if settings.debug:
                logger.error(
                    "Error de conexión con Ollama: %s", str(exc)
                )
            return (
                "No pude comunicarme con el modelo de IA local en este momento. "
                "Verifica que Ollama esté en ejecución y vuelve a intentarlo."
            )

        except Exception as exc:  # noqa: BLE001
            if settings.debug:
                logger.exception("Error inesperado al llamar al modelo de IA: %s", str(exc))
            return (
                "Ocurrió un error inesperado al generar la respuesta. "
                "Por favor, intenta nuevamente más tarde."
            )
        finally:
            duracion = perf_counter() - inicio
            if settings.debug:
                logger.info(
                    "LLM: duración=%.2fs, len_prompt=%d, max_tokens=%d",
                    duracion,
                    len(prompt),
                    settings.max_tokens_respuesta,
                )
