from fastapi import FastAPI

from app.core.config import settings
from app.api.rutas_tutor import enrutador as enrutador_tutor

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


# Rutas del tutor educativo
app.include_router(enrutador_tutor, prefix="/api")
