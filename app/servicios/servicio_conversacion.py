from dataclasses import dataclass
from datetime import datetime
from typing import List

from app.utilidades.util_tiempo import obtener_ahora_utc, es_mayor_a_dias


_DIAS_MAXIMOS_CONVERSACION = 2


@dataclass
class MensajeConversacion:
    rol: str              # "usuario" o "tutor"
    contenido: str
    marca_tiempo: datetime


_conversacion: List[MensajeConversacion] = []


def _limpiar_conversacion_expirada() -> None:
    """
    Elimina los mensajes cuya antigüedad sea mayor a _DIAS_MAXIMOS_CONVERSACION.
    """
    global _conversacion
    _conversacion = [
        mensaje
        for mensaje in _conversacion
        if not es_mayor_a_dias(mensaje.marca_tiempo, _DIAS_MAXIMOS_CONVERSACION)
    ]


def agregar_mensaje(rol: str, contenido: str) -> None:
    """
    Agrega un mensaje a la conversación y limpia mensajes expirados.
    """
    _limpiar_conversacion_expirada()
    mensaje = MensajeConversacion(
        rol=rol,
        contenido=contenido,
        marca_tiempo=obtener_ahora_utc(),
    )
    _conversacion.append(mensaje)


def obtener_conversacion() -> List[MensajeConversacion]:
    """
    Devuelve la conversación completa vigente tras limpiar mensajes expirados.
    """
    _limpiar_conversacion_expirada()
    return list(_conversacion)


def reiniciar_conversacion() -> None:
    """
    Elimina todos los mensajes almacenados en la conversación.
    """
    global _conversacion
    _conversacion = []
