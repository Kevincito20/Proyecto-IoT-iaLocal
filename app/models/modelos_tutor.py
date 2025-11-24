from typing import Optional, Literal, List

from pydantic import BaseModel


class Mensaje(BaseModel):
    rol: Literal["usuario", "asistente", "sistema"]
    contenido: str


class SolicitudTutor(BaseModel):
    mensaje: str
    materia: Optional[str] = None
    mensajes_anteriores: Optional[List[Mensaje]] = None


class RespuestaTutor(BaseModel):
    respuesta: str
    materia_detectada: Optional[str] = None
    es_tarea_sin_contexto: bool = False
