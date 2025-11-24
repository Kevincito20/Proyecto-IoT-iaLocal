# Asistente IA Local Educativo

Asistente de IA educativo que funciona de forma local usando FastAPI y Ollama (modelo phi3:mini), diseñado para correr en Raspberry Pi 5 (8GB RAM).

## Cómo levantar el servidor (entorno de desarrollo)

```bash
venv\Scripts\activate
uvicorn app.principal:app --reload --host 0.0.0.0 --port 8000
