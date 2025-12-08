from datetime import datetime, timedelta, timezone


def obtener_ahora_utc() -> datetime:
    """
    Devuelve la fecha y hora actual en UTC.
    """
    return datetime.now(timezone.utc)


def es_mayor_a_dias(fecha: datetime, dias: int) -> bool:
    """
    Indica si ha pasado más del número de días indicado desde la fecha dada.
    """
    ahora = obtener_ahora_utc()
    return ahora - fecha > timedelta(days=dias)
