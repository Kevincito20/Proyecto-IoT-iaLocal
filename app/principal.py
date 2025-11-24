from fastapi import FastAPI
from app.core.config import settings

app = FastAPI(title=settings.app_name)


@app.get("/", tags=["sistema"])
def read_root():
    return {"mensaje": "Asistente IA Local funcionando correctamente 🚀"}


@app.get("/health", tags=["sistema"])
def health_check():
    return {
        "status": "ok",
        "environment": settings.environment,
        "debug": settings.debug,
    }
