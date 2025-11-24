import os
from dataclasses import dataclass
from functools import lru_cache

from dotenv import load_dotenv

# Cargar variables desde .env (si existe)
load_dotenv()


def str_to_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "t", "yes", "y", "si", "sí"}


def str_to_int(value: str | None, default: int) -> int:
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        return default


def str_to_float(value: str | None, default: float) -> float:
    if value is None:
        return default
    try:
        return float(value)
    except ValueError:
        return default


@dataclass
class Settings:
    app_name: str
    debug: bool
    environment: str

    ollama_host: str
    ollama_modelo: str
    max_tokens_respuesta: int
    ollama_timeout_segundos: float
    temperatura_modelo: float

    # Optimizaciones para Raspberry / rendimiento
    max_mensajes_historial: int
    max_concurrencia_llm: int


@lru_cache
def get_settings() -> Settings:
    return Settings(
        app_name=os.getenv("APP_NAME", "Asistente IA Local Educativo"),
        debug=str_to_bool(os.getenv("DEBUG"), True),
        environment=os.getenv("ENVIRONMENT", "development"),

        ollama_host=os.getenv("OLLAMA_HOST", "http://localhost:11434"),
        ollama_modelo=os.getenv("OLLAMA_MODELO", "phi3:mini"),
        max_tokens_respuesta=str_to_int(
            os.getenv("MAX_TOKENS_RESPUESTA"), 256
        ),
        ollama_timeout_segundos=str_to_float(
            os.getenv("OLLAMA_TIMEOUT_SEGUNDOS"), 60.0
        ),
        temperatura_modelo=str_to_float(
            os.getenv("TEMPERATURA_MODELO"), 0.7
        ),

        # Para no explotar la RAM ni la CPU de la Raspberry
        max_mensajes_historial=str_to_int(
            os.getenv("MAX_MENSAJES_HISTORIAL"), 4
        ),
        max_concurrencia_llm=str_to_int(
            os.getenv("MAX_CONCURRENCIA_LLM"), 1
        ),
    )


settings = get_settings()
