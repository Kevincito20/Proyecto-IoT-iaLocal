import os
from dotenv import load_dotenv


class Ajustes:
    """
    Carga y expone las variables de configuración del sistema.
    """

    def __init__(self) -> None:
        load_dotenv()

        self.url_ollama_generar: str = os.getenv(
            "URL_OLLAMA_GENERAR",
            "http://localhost:11434/api/generate",
        )
        self.url_ollama_tags: str = os.getenv(
            "URL_OLLAMA_TAGS",
            "http://localhost:11434/api/tags",
        )
        self.modelo_ollama: str = os.getenv(
            "MODELO_OLLAMA",
            "phi3:mini",
        )
        self.temperatura_por_defecto: float = float(
            os.getenv("TEMPERATURA_POR_DEFECTO", "0.7")
        )
        self.maximo_tokens: int = int(os.getenv("MAXIMO_TOKENS", "1024"))
        self.token_api: str = os.getenv("TOKEN_API", "")


ajustes = Ajustes()
