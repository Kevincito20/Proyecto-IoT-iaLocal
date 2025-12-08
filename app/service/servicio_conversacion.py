from dataclasses import dataclass, field
from datetime import datetime
from typing import List

from app.utils.util_tiempo import obtener_ahora_utc, es_mayor_a_dias


_DIAS_MAXIMOS_CONVERSACION = 3
_MAXIMO_CONVERSACIONES = 3


@dataclass
class MensajeConversacion:
    rol: str              # "usuario" o "tutor"
    contenido: str
    marca_tiempo: datetime


@dataclass
class Conversacion:
    id_conversacion: int
    fecha_inicio: datetime
    mensajes: List[MensajeConversacion] = field(default_factory=list)


_conversaciones: List[Conversacion] = []
_conversacion_actual_id: int | None = None
_siguiente_id_conversacion: int = 1


def _limpiar_conversaciones_expiradas() -> None:
    """
    Elimina las conversaciones cuya antigüedad sea mayor a _DIAS_MAXIMOS_CONVERSACION.
    """
    global _conversaciones, _conversacion_actual_id

    ahora = obtener_ahora_utc()
    conversaciones_vigentes: List[Conversacion] = []

    for conversacion in _conversaciones:
        if es_mayor_a_dias(conversacion.fecha_inicio, _DIAS_MAXIMOS_CONVERSACION):
            continue
        conversaciones_vigentes.append(conversacion)

    _conversaciones = conversaciones_vigentes

    if _conversacion_actual_id is not None:
        existe = any(c.id_conversacion == _conversacion_actual_id for c in _conversaciones)
        if not existe:
            _conversacion_actual_id = None


def _aplicar_limite_maximo() -> None:
    """
    Mantiene como máximo _MAXIMO_CONVERSACIONES conversaciones,
    conservando las más recientes por fecha de inicio.
    """
    global _conversaciones, _conversacion_actual_id

    if len(_conversaciones) <= _MAXIMO_CONVERSACIONES:
        return

    _conversaciones.sort(key=lambda c: c.fecha_inicio)

    while len(_conversaciones) > _MAXIMO_CONVERSACIONES:
        eliminada = _conversaciones.pop(0)
        if eliminada.id_conversacion == _conversacion_actual_id:
            if _conversaciones:
                _conversacion_actual_id = _conversaciones[-1].id_conversacion
            else:
                _conversacion_actual_id = None


def _obtener_conversacion_actual() -> Conversacion:
    """
    Devuelve la conversación actual. Si no existe, crea una nueva.
    Aplica limpieza de conversaciones expiradas y el límite máximo.
    """
    global _conversaciones, _conversacion_actual_id, _siguiente_id_conversacion

    _limpiar_conversaciones_expiradas()

    if _conversacion_actual_id is not None:
        for conversacion in _conversaciones:
            if conversacion.id_conversacion == _conversacion_actual_id:
                return conversacion

    nueva_conversacion = Conversacion(
        id_conversacion=_siguiente_id_conversacion,
        fecha_inicio=obtener_ahora_utc(),
    )
    _siguiente_id_conversacion += 1

    _conversaciones.append(nueva_conversacion)
    _aplicar_limite_maximo()

    _conversacion_actual_id = nueva_conversacion.id_conversacion
    return nueva_conversacion


def agregar_mensaje(rol: str, contenido: str) -> None:
    """
    Agrega un mensaje a la conversación actual.
    """
    conversacion = _obtener_conversacion_actual()
    conversacion.mensajes.append(
        MensajeConversacion(
            rol=rol,
            contenido=contenido,
            marca_tiempo=obtener_ahora_utc(),
        )
    )


def obtener_conversacion_actual() -> List[MensajeConversacion]:
    """
    Devuelve la lista de mensajes de la conversación actual.
    """
    conversacion = _obtener_conversacion_actual()
    return list(conversacion.mensajes)


def reiniciar_conversacion() -> None:
    """
    Inicia una nueva conversación y mantiene las anteriores
    dentro del límite de cantidad y de días.
    """
    global _conversacion_actual_id
    _conversacion_actual_id = None
    _obtener_conversacion_actual()


def obtener_resumen_conversaciones() -> List[dict]:
    """
    Devuelve un resumen de las conversaciones almacenadas,
    usado principalmente para depuración y pruebas internas.
    (Devuelve fecha_inicio como datetime, no serializable directo en JSON.)
    """
    _limpiar_conversaciones_expiradas()
    return [
        {
            "id_conversacion": c.id_conversacion,
            "fecha_inicio": c.fecha_inicio,
            "cantidad_mensajes": len(c.mensajes),
        }
        for c in _conversaciones
    ]


# ========= NUEVAS FUNCIONES PARA LA UI Y LA API =========


def obtener_conversacion_por_id(id_conversacion: int) -> Conversacion | None:
    """
    Devuelve una conversación por id, o None si no existe.
    Aplica limpieza de conversaciones expiradas.
    """
    _limpiar_conversaciones_expiradas()
    for conversacion in _conversaciones:
        if conversacion.id_conversacion == id_conversacion:
            return conversacion
    return None


def establecer_conversacion_actual(id_conversacion: int) -> bool:
    """
    Establece la conversación actual a partir de su id.
    Devuelve True si se encontró y asignó, False en caso contrario.
    """
    global _conversacion_actual_id

    _limpiar_conversaciones_expiradas()

    for conversacion in _conversaciones:
        if conversacion.id_conversacion == id_conversacion:
            _conversacion_actual_id = id_conversacion
            return True

    return False


def obtener_resumen_conversaciones_completo() -> dict:
    """
    Devuelve un resumen de las conversaciones y la conversación actual,
    listo para ser devuelto por una API (fechas en formato texto).
    """
    _limpiar_conversaciones_expiradas()

    resumen = [
        {
            "id_conversacion": c.id_conversacion,
            "fecha_inicio": c.fecha_inicio.isoformat(),
            "cantidad_mensajes": len(c.mensajes),
        }
        for c in _conversaciones
    ]

    return {
        "conversaciones": resumen,
        "id_actual": _conversacion_actual_id,
    }
