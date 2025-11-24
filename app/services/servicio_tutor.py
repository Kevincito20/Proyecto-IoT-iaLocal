from typing import Optional, List

from app.models.modelos_tutor import Mensaje
from app.services.servicio_prompt import construir_prompt_pedagogico
from app.services.servicio_llm import generar_respuesta_ia


PALABRAS_PROHIBIDAS = {
    "suicidio", "matar", "asesinar", "violación", "violacion",
    "pornografía", "porno", "drogas fuertes", "droga fuerte",
    "terrorismo", "bombas", "explosivos", "homicidio", "asesinato",
    "secuestrar", "secuestro", "trafico de personas", "tráfico de personas",
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
    """Normaliza un texto quitando espacios y pasando a minúsculas."""
    return texto.strip().lower()


def _detectar_palabras_prohibidas(texto: str) -> bool:
    """
    Devuelve True si el texto contiene alguna palabra prohibida.

    Se usa para bloquear contenido sensible o inapropiado.
    """
    texto_min = texto.lower()
    return any(palabra in texto_min for palabra in PALABRAS_PROHIBIDAS)


def _detectar_materia(materia: Optional[str]) -> Optional[str]:
    """
    Devuelve la materia normalizada si se reconoce, o None si no.
    """
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
    """
    Determina si la solicitud del estudiante parece ser una tarea
    con poco o ningún contexto.

    Esto se usa para ajustar el comportamiento pedagógico
    (por ejemplo, pedir que el modelo no haga solo la tarea).
    """
    texto = mensaje.strip()

    # Operadores típicos de ejercicios matemáticos/físicos
    if len(texto) < 40 and any(s in texto for s in ["=", "/", "√", "^", "+", "-"]):
        return True

    # Muy poca longitud en general: probablemente no hay contexto
    if len(texto) < LONGITUD_MIN_TAREA:
        return True

    texto_minus = texto.lower()
    if texto_minus.startswith("resuelve") or texto_minus.startswith("haz la tarea"):
        return True

    return False


async def tutor(
    mensaje: str,
    materia: Optional[str] = None,
    mensajes_anteriores: Optional[List[Mensaje]] = None,
) -> str:
    """
    Lógica principal del tutor educativo.

    Responsabilidades:
    - Validar la entrada del usuario (longitud, contenido vacío).
    - Aplicar filtros de seguridad (palabras prohibidas).
    - Detectar materia y si la solicitud parece tarea sin contexto.
    - Construir un prompt pedagógico usando el historial de conversación.
    - Llamar al modelo de IA local a través de generar_respuesta_ia().

    Devuelve un texto en español listo para mostrarse al estudiante.
    """

    mensaje_limpio = mensaje.strip()

    # Validación básica: mensaje vacío
    if not mensaje_limpio:
        return (
            "No has proporcionado ninguna pregunta o tarea. "
            "Por favor, ingresa una pregunta o ejercicio para que pueda ayudarte."
        )

    # Longitud máxima para proteger recursos (especialmente en Raspberry Pi)
    if len(mensaje_limpio) > LONGITUD_MAXIMA_PREGUNTA:
        return (
            f"La pregunta o tarea es demasiado larga. "
            f"Por favor, limita tu entrada a {LONGITUD_MAXIMA_PREGUNTA} caracteres."
        )

    # Filtro de contenido sensible
    if _detectar_palabras_prohibidas(mensaje_limpio):
        return (
            "Lo siento, no puedo ayudarte con esa solicitud debido a la naturaleza del contenido. "
            "Si tienes una duda personal o emocional, es mejor que hables con "
            "un adulto de confianza, como tu docente, un familiar o el orientador "
            "de la escuela."
        )

    # Detección de materia y tarea sin contexto
    materia_detectada = _detectar_materia(materia)
    tarea_sin_contexto = es_tarea_sin_contexto(mensaje_limpio)

    # Construcción del prompt pedagógico,
    # incluyendo historial si viene en mensajes_anteriores
    prompt = construir_prompt_pedagogico(
        mensaje_usuario=mensaje_limpio,
        materia_norm=materia_detectada,
        es_tarea_sin_contexto=tarea_sin_contexto,
        mensajes_anteriores=mensajes_anteriores,
    )

    # Llamada al modelo de IA local (Ollama + phi3:mini, configurado en servicio_llm)
    respuesta_ia = await generar_respuesta_ia(prompt)

    return respuesta_ia
