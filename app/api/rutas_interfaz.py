from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import HTMLResponse


enrutador_interfaz = APIRouter(tags=["interfaz"])


@enrutador_interfaz.get("/", response_class=HTMLResponse)
async def mostrar_interfaz():
    """
    Devuelve la interfaz HTML de prueba para el chat.
    """
    ruta_base = Path(__file__).resolve().parent.parent
    ruta_recurso = ruta_base / "resource" / "interfaz.html"

    return ruta_recurso.read_text(encoding="utf-8")
