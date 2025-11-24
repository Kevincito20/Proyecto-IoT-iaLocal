from typing import Optional

from app.services.servicio_llm import generar_respuesta_ia
from app.services.servicio_prompt import construir_prompt_pedagogico

PALABRAS_PROHIBIDAS = {
    "suicidio", "matar", "asesinar", "violación", "violacion",
    "pornografía", "porno", "drogas fuertes", "droga fuerte",
    "terrorismo", "bombas", "explosivos", "homicidio", "asesinato",
    "secuestrar", "secuestro", "trafico de personas"
}

MATERIAS_RECONOCIDAS = {
    "matematicas": "matemáticas",
    "matemáticas": "matemáticas",
    "mates": "matemáticas",
    "ciencias": "ciencias",
    "ciencias naturales": "ciencias naturales",
    "fisica": "física",
    "física": "física",
    "quimica": "química",
    "química": "química",
    "biologia": "biología",
    "biología": "biología",
    "español": "español",
    "lengua": "español",
    "historia": "historia",
    "geografia": "geografía",
    "geografía": "geografía",
    "ingles": "inglés",
    "inglés": "inglés",
}

LONGITUD_MAXIMA_PREGUNTA = 500
LONGITUD_MIN_TAREA = 15


def _normalizar_texto(texto: str) -> str:
    return texto.strip().lower()


def _detectar_palabras_prohibidas(texto: str) -> bool:
    """Devuelve True si el texto contiene alguna palabra prohibida."""
    texto_min = texto.lower()
    return any(palabra in texto_min for palabra in PALABRAS_PROHIBIDAS)


def _detectar_materia(materia: Optional[str]) -> Optional[str]:
    if not materia:
        return None

    materia_min = _normalizar_texto(materia)
    return MATERIAS_RECONOCIDAS.get(materia_min)


def obtener_materia_normalizada(materia: Optional[str]) -> Optional[str]:
    """
    Función pública para que otras partes del sistema
    puedan reutilizar la detección de materia.
    """
    return _detectar_materia(materia)


def es_tarea_sin_contexto(mensaje: str) -> bool:
    texto = mensaje.strip()

    if len(texto) < 40 and any(s in texto for s in ["=", "/", "√", "^", "+", "-"]):
        return True

    if len(texto) < LONGITUD_MIN_TAREA:
        return True

    texto_minus = texto.lower()
    if texto_minus.startswith("resuelve") or texto_minus.startswith("haz la tarea"):
        return True

    return False


async def tutor(mensaje: str, materia: Optional[str] = None) -> str:
    """
    Lógica principal del tutor educativo.

    - Valida la entrada y aplica filtros de seguridad.
    - Si el contenido es adecuado, construye un prompt pedagógico
      y llama al modelo de IA local (Ollama) a través de un servicio LLM.
    """

    mensaje_limpio = mensaje.strip()

    if not mensaje_limpio:
        return (
            "No has proporcionado ninguna pregunta o tarea. "
            "Por favor, ingresa una pregunta o ejercicio para que pueda ayudarte."
        )

    if len(mensaje_limpio) > LONGITUD_MAXIMA_PREGUNTA:
        return (
            f"La pregunta o tarea es demasiado larga. "
            f"Por favor, limita tu entrada a {LONGITUD_MAXIMA_PREGUNTA} caracteres."
        )

    if _detectar_palabras_prohibidas(mensaje_limpio):
        return (
            "Lo siento, no puedo ayudarte con esa solicitud debido a la naturaleza del contenido. "
            "Si tienes una duda personal o emocional, es mejor que hables con "
            "un adulto de confianza, como tu docente, un familiar o el orientador "
            "de la escuela."
        )

    materia_detectada = _detectar_materia(materia)
    tarea_sin_contexto = es_tarea_sin_contexto(mensaje_limpio)

    prompt = construir_prompt_pedagogico(
        mensaje_usuario=mensaje_limpio,
        materia_norm=materia_detectada,
        es_tarea_sin_contexto=tarea_sin_contexto,
    )

    # FASE 2: aún NO usamos un modelo real.
    # generar_respuesta_ia devolverá un mensaje simulado.
    respuesta_ia = await generar_respuesta_ia(prompt)

    return respuesta_ia
