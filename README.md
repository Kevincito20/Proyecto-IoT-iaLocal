# 🧠 Proyecto de IA Local Educativa  
### Tutor académico local ejecutándose en Raspberry Pi 5 y accesible desde ESP32

Este proyecto implementa un **sistema de inteligencia artificial local**, enfocado en funciones educativas, capaz de:

- Procesar preguntas académicas del usuario.
- Mantener contexto conversacional limitado.
- Generar respuestas en tiempo real (streaming).
- Guardar conversaciones recientes durante un máximo de 3 días.
- Servir una interfaz web alojada en el ESP32 o desde el propio backend.
- Operar totalmente offline si se requiere.

El backend corre en una **Raspberry Pi 5** utilizando **FastAPI** y el modelo **Phi-3 Mini (Ollama)**.

El **ESP32** almacena y sirve la interfaz web, enviando solicitudes al Raspberry Pi para obtener respuestas.

La arquitectura es ligera, optimizada y segura para funcionar en hardware de bajos recursos.

---

# 🔥 Características principales

### ✔ IA COMPLETAMENTE LOCAL
No requiere conexión a Internet.  
Toda la inferencia se realiza dentro del Raspberry Pi (Ollama).

### ✔ STREAMING TOKEN POR TOKEN
Las respuestas se generan en tiempo real:



### ✔ CONTEXTO DE CONVERSACIÓN OPTIMIZADO
- Máximo de **3 conversaciones activas**.
- Cada conversación se almacena **solo por 3 días**.
- Sin base de datos; almacenamiento en memoria.
- Contexto reducido para optimizar memoria RAM.

### ✔ INTERFAZ ELEGANTE TIPO CHATGPT
- UI moderna y minimalista.
- Soporte para carga de conversaciones recientes.
- Reinicio de conversación.
- Compatible con escritorio, móvil y con ESP32.

### ✔ ARQUITECTURA MODULAR
- Servicios desacoplados (Ollama / Tutor / Conversaciones).
- Endpoints limpios.
- Seguridad por token API.
- Código altamente legible y mantenible.

---

# 🏗 Arquitectura General

       ┌────────────────────────┐
       │       ESP32 (UI)       │
       │  Sirve interfaz HTML   │
       └────────────┬───────────┘
                    │ HTTP
                    ▼
          ┌──────────────────────┐
          │ Raspberry Pi 5       │
          │ Backend FastAPI      │
          │ Servicio de Tutor    │
          │ Gestión de sesiones  │
          └──────────┬───────────┘
                    │ Localhost API
                    ▼
      ┌─────────────────────────────┐
      │ OLLAMA (Modelo Phi-3 Mini)  │
      │ Generación de respuestas    │
      └─────────────────────────────┘
