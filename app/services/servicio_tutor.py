from typing import Optional, List, Tuple

from app.models.modelos_tutor import Mensaje
from app.services.servicio_prompt import construir_prompt_pedagogico
from app.services.servicio_llm import generar_respuesta_ia


# ----------------------------
# Listas de palabras sensibles
# ----------------------------

PALABRAS_AUTODANO = {
    "suicidio",
    "suicidarme",
    "matarme",
    "hacerme daño",
    "autolesion",
    "autolesión",
    "quiero morir",
    "no quiero vivir",
}

PALABRAS_VIOLENCIA_GRAVE = {
    "matar",
    "asesinar",
    "asesinato",
    "homicidio",
    "tortura",
    "golpear hasta",
    "violación",
    "violacion",
    "secuestrar",
    "secuestro",
}

PALABRAS_SEXUALES_EXPLICITAS = {
    "pornografía",
    "pornografia",
    "porno",
    "sexo explicito",
    "sexo explícito",
    "sexual infantil",
}

PALABRAS_DROGAS = {
    "drogas fuertes",
    "droga fuerte",
    "cocaína",
    "cocaina",
    "heroína",
    "heroina",
    "metanfetamina",
}

PALABRAS_TERRORISMO = {
    "terrorismo",
    "bomba",
    "bombas",
    "explosivos",
    "fabricar bomba",
}

# Combina todo para comprobaciones generales si hiciera falta
PALABRAS_PROHIBIDAS = (
    PALABRAS_AUTODANO
    | PALABRAS_VIOLENCIA_GRAVE
    | PALABRAS_SEXUALES_EXPLICITAS
    | PALABRAS_DROGAS
    | PALABRAS_TERRORISMO
)

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


# ----------------------------
# Funciones auxiliares
# ----------------------------

def _normalizar_texto(texto: str) -> str:
    """Normaliza un texto quitando espacios y pasando a minúsculas."""
    return texto.strip().lower()


def _detectar_categoria_contenido_no_educativo(texto: str) -> Tuple[bool, Optional[str]]:
    """
    Detecta si el texto contiene contenido sensible/no educativo.
    Devuelve (True, categoria) si debe bloquearse, o (False, None) si no.
    """
    t = texto.lower()

    # Orden aproximado por gravedad
    for palabra in PALABRAS_AUTODANO:
        if palabra in t:
            return True, "autodaño"

    for palabra in PALABRAS_VIOLENCIA_GRAVE:
        if palabra in t:
            return True, "violencia grave"

    for palabra in PALABRAS_SEXUALES_EXPLICITAS:
        if palabra in t:
            return True, "contenido sexual explícito"

    for palabra in PALABRAS_DROGAS:
        if palabra in t:
            return True, "drogas ilegales"

    for palabra in PALABRAS_TERRORISMO:
        if palabra in t:
            return True, "terrorismo o uso de explosivos"

    return False, None


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


# ----------------------------
# Lógica principal del tutor
# ----------------------------

async def tutor(
    mensaje: str,
    materia: Optional[str] = None,
    mensajes_anteriores: Optional[List[Mensaje]] = None,
) -> str:
    """
    Lógica principal del tutor educativo.

    Responsabilidades:
    - Validar la entrada del usuario (longitud, contenido vacío).
    - Aplicar filtros de seguridad (contenido sensible).
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

    # Filtro de contenido sensible / no educativo
    hay_contenido_no_educativo, categoria = _detectar_categoria_contenido_no_educativo(
        mensaje_limpio
    )
    if hay_contenido_no_educativo:
        if categoria == "autodaño":
            return (
                "Parece que estás hablando de hacerte daño o de no querer seguir viviendo. "
                "Lamento que te sientas así, pero no puedo ayudarte con este tipo de solicitud. "
                "Es muy importante que hables con un adulto de confianza, como tu docente, "
                "un familiar cercano o el orientador de la escuela. "
                "Si en tu país existe una línea de ayuda emocional, también puede ser una buena opción."
            )

        return (
            "Lo siento, no puedo ayudarte con esa solicitud debido a la naturaleza del contenido "
            f"({categoria}). Este asistente está pensado solo para apoyar en temas educativos. "
            "Si tienes dudas académicas o necesitas ayuda con alguna materia, con gusto puedo ayudarte."
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
