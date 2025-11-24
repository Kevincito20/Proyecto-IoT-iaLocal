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


@dataclass
class Settings:
    app_name: str
    debug: bool
    environment: str


@lru_cache
def get_settings() -> Settings:
    return Settings(
        app_name=os.getenv("APP_NAME", "Asistente IA Local Educativo"),
        debug=str_to_bool(os.getenv("DEBUG"), True),
        environment=os.getenv("ENVIRONMENT", "development"),
    )


settings = get_settings()
