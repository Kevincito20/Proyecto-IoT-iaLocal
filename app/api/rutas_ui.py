from fastapi import APIRouter
from fastapi.responses import HTMLResponse

enrutador_ui = APIRouter(prefix="/ui", tags=["ui"])


@enrutador_ui.get("/tutor", response_class=HTMLResponse)
async def pagina_tutor() -> str:
    """
    Página sencilla de interfaz web para el tutor educativo.
    No usa plantillas ni frameworks, solo HTML + CSS + JS básicos.
    """
    return """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8" />
    <title>Asistente IA Local - Tutor Educativo</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <style>
        :root {
            --color-fondo: #0f172a;
            --color-secundario: #1f2937;
            --color-detalle: #3b82f6;
            --color-texto: #e5e7eb;
            --color-texto-suave: #9ca3af;
            --color-usuario: #22c55e;
            --color-error: #f97373;
        }

        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            background: radial-gradient(circle at top, #1e293b 0, #020617 50%, #000 100%);
            color: var(--color-texto);
            display: flex;
            justify-content: center;
            align-items: stretch;
            min-height: 100vh;
        }

        .contenedor-principal {
            width: 100%;
            max-width: 960px;
            margin: 16px;
            background: rgba(15, 23, 42, 0.9);
            border-radius: 16px;
            border: 1px solid rgba(148, 163, 184, 0.4);
            box-shadow: 0 20px 50px rgba(15, 23, 42, 0.8);
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }

        .encabezado {
            padding: 16px 20px;
            border-bottom: 1px solid rgba(148, 163, 184, 0.3);
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 8px;
        }

        .titulo {
            display: flex;
            flex-direction: column;
            gap: 4px;
        }

        .titulo h1 {
            font-size: 1.1rem;
            margin: 0;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .titulo h1 span.logo {
            display: inline-flex;
            width: 22px;
            height: 22px;
            border-radius: 999px;
            background: radial-gradient(circle at 30% 30%, #bfdbfe, #3b82f6, #0f172a);
            box-shadow: 0 0 12px rgba(59, 130, 246, 0.8);
        }

        .titulo p {
            margin: 0;
            font-size: 0.8rem;
            color: var(--color-texto-suave);
        }

        .acciones {
            display: flex;
            gap: 8px;
            align-items: center;
        }

        .boton {
            border: none;
            border-radius: 999px;
            padding: 6px 12px;
            font-size: 0.8rem;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(15, 23, 42, 0.7);
            color: var(--color-texto-suave);
            border: 1px solid rgba(148, 163, 184, 0.4);
            transition: background 0.2s ease, border-color 0.2s ease, transform 0.1s ease;
        }

        .boton:hover {
            background: rgba(30, 64, 175, 0.9);
            border-color: rgba(59, 130, 246, 0.8);
            color: #e5e7eb;
            transform: translateY(-1px);
        }

        .boton-primario {
            background: linear-gradient(135deg, #3b82f6, #22c55e);
            color: #0b1120;
            border-color: transparent;
            font-weight: 600;
        }

        .boton-primario:hover {
            background: linear-gradient(135deg, #60a5fa, #4ade80);
        }

        .contenido {
            display: grid;
            grid-template-columns: minmax(0, 2.5fr) minmax(0, 1.3fr);
            gap: 0;
            min-height: 380px;
        }

        @media (max-width: 800px) {
            .contenido {
                grid-template-columns: minmax(0, 1fr);
            }
        }

        .panel-chat {
            border-right: 1px solid rgba(30, 64, 175, 0.5);
            display: flex;
            flex-direction: column;
            min-height: 260px;
        }

        @media (max-width: 800px) {
            .panel-chat {
                border-right: none;
                border-bottom: 1px solid rgba(30, 64, 175, 0.5);
            }
        }

        .mensajes {
            flex: 1;
            padding: 16px 20px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .mensaje {
            max-width: 90%;
            padding: 10px 12px;
            border-radius: 12px;
            font-size: 0.9rem;
            line-height: 1.4;
            position: relative;
        }

        .mensaje-usuario {
            align-self: flex-end;
            background: rgba(34, 197, 94, 0.12);
            border: 1px solid rgba(34, 197, 94, 0.6);
        }

        .mensaje-asistente {
            align-self: flex-start;
            background: rgba(15, 23, 42, 0.9);
            border: 1px solid rgba(59, 130, 246, 0.6);
        }

        .mensaje-error {
            align-self: center;
            background: rgba(239, 68, 68, 0.12);
            border-color: rgba(248, 113, 113, 0.8);
            color: #fecaca;
        }

        .mensaje small {
            display: block;
            margin-bottom: 4px;
            font-size: 0.7rem;
            opacity: 0.7;
        }

        .mensaje pre {
            margin: 4px 0 0;
            white-space: pre-wrap;
            word-wrap: break-word;
        }

        .panel-entrada {
            padding: 10px 16px 14px;
            border-top: 1px solid rgba(148, 163, 184, 0.3);
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        .fila-entrada {
            display: flex;
            gap: 8px;
            align-items: flex-end;
        }

        .entrada-texto {
            flex: 1;
            border-radius: 12px;
            border: 1px solid rgba(148, 163, 184, 0.6);
            padding: 8px 10px;
            background: rgba(15, 23, 42, 0.9);
            color: var(--color-texto);
            font-size: 0.9rem;
            resize: none;
            min-height: 42px;
            max-height: 110px;
        }

        .entrada-texto:focus {
            outline: none;
            border-color: rgba(59, 130, 246, 0.9);
            box-shadow: 0 0 0 1px rgba(59, 130, 246, 0.7);
        }

        .panel-opciones {
            padding: 16px 16px 16px 18px;
            display: flex;
            flex-direction: column;
            gap: 12px;
            background: radial-gradient(circle at top, rgba(30, 64, 175, 0.35), transparent 55%);
        }

        .grupo-opcion {
            display: flex;
            flex-direction: column;
            gap: 4px;
        }

        .grupo-opcion label {
            font-size: 0.8rem;
            color: var(--color-texto-suave);
        }

        .grupo-opcion select {
            border-radius: 999px;
            border: 1px solid rgba(148, 163, 184, 0.6);
            padding: 5px 10px;
            background: rgba(15, 23, 42, 0.9);
            color: var(--color-texto);
            font-size: 0.85rem;
        }

        .grupo-opcion select:focus {
            outline: none;
            border-color: rgba(59, 130, 246, 0.9);
            box-shadow: 0 0 0 1px rgba(59, 130, 246, 0.7);
        }

        .texto-ayuda {
            font-size: 0.75rem;
            color: var(--color-texto-suave);
        }

        .estado {
            font-size: 0.75rem;
            color: var(--color-texto-suave);
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .indicador {
            width: 7px;
            height: 7px;
            border-radius: 999px;
            background: #16a34a;
            box-shadow: 0 0 4px #22c55e;
        }

        .indicador-ocupado {
            background: #f97316;
            box-shadow: 0 0 4px #fdba74;
        }

        .indicador-error {
            background: #ef4444;
            box-shadow: 0 0 4px #fca5a5;
        }

        .badge {
            font-size: 0.65rem;
            padding: 2px 6px;
            border-radius: 999px;
            background: rgba(15, 23, 42, 0.9);
            border: 1px solid rgba(148, 163, 184, 0.6);
        }
    </style>
</head>
<body>
<div class="contenedor-principal">
    <header class="encabezado">
        <div class="titulo">
            <h1>
                <span class="logo"></span>
                Asistente IA Local - Tutor Educativo
            </h1>
            <p>Funciona con un modelo local (Ollama + phi3:mini) optimizado para explicaciones paso a paso.</p>
        </div>
        <div class="acciones">
            <span class="badge" id="textoModelo">Modelo: phi3:mini</span>
            <button class="boton" type="button" id="botonNuevoChat">
                🧹 Nuevo chat
            </button>
        </div>
    </header>

    <main class="contenido">
        <section class="panel-chat">
            <div class="mensajes" id="areaMensajes">
                <div class="mensaje mensaje-asistente">
                    <small>Tutor</small>
                    <pre>Hola, soy tu tutor educativo local. Puedo ayudarte a entender mejor temas de distintas materias
como matemáticas, ciencias, historia, etc. Escribe tu duda o ejercicio y lo vemos juntos 🙂</pre>
                </div>
            </div>

            <div class="panel-entrada">
                <div class="fila-entrada">
                    <textarea
                        id="entradaMensaje"
                        class="entrada-texto"
                        placeholder="Escribe tu pregunta o ejercicio aquí..."
                    ></textarea>
                    <button class="boton boton-primario" type="button" id="botonEnviar">
                        Enviar
                    </button>
                </div>
                <div class="estado" id="textoEstado">
                    <span class="indicador" id="indicadorEstado"></span>
                    Listo para ayudarte.
                </div>
            </div>
        </section>

        <aside class="panel-opciones">
            <div class="grupo-opcion">
                <label for="selectMateria">Materia (opcional)</label>
                <select id="selectMateria">
                    <option value="">— Sin materia específica —</option>
                    <option value="matematicas">Matemáticas</option>
                    <option value="ciencias">Ciencias</option>
                    <option value="ciencias naturales">Ciencias naturales</option>
                    <option value="fisica">Física</option>
                    <option value="quimica">Química</option>
                    <option value="biologia">Biología</option>
                    <option value="español">Español / Lengua</option>
                    <option value="historia">Historia</option>
                    <option value="geografia">Geografía</option>
                    <option value="ingles">Inglés</option>
                </select>
            </div>
            <div class="grupo-opcion">
                <label>Nivel sugerido</label>
                <p class="texto-ayuda">
                    Por ahora el tutor se adapta de forma general. Más adelante se puede ampliar
                    para nivel primaria, secundaria o universitario.
                </p>
            </div>
            <div class="grupo-opcion">
                <label>Consejos de uso</label>
                <ul class="texto-ayuda" style="padding-left: 16px; margin: 0;">
                    <li>Incluye lo más posible el contexto de tu duda.</li>
                    <li>Si es un ejercicio, di qué parte no entiendes.</li>
                    <li>Puedes continuar la conversación sin volver a repetir todo.</li>
                    <li>Evita contenido no educativo o peligroso.</li>
                </ul>
            </div>
        </aside>
    </main>
</div>

<script>
    (function () {
        const areaMensajes = document.getElementById("areaMensajes");
        const entradaMensaje = document.getElementById("entradaMensaje");
        const botonEnviar = document.getElementById("botonEnviar");
        const botonNuevoChat = document.getElementById("botonNuevoChat");
        const selectMateria = document.getElementById("selectMateria");
        const textoEstado = document.getElementById("textoEstado");
        const indicadorEstado = document.getElementById("indicadorEstado");

        /** Historial que se envía al backend como mensajes_anteriores */
        let mensajesAnteriores = [];
        const LIMITE_HISTORIAL = 6;

        function actualizarEstado(texto, modo) {
            textoEstado.textContent = texto;
            indicadorEstado.classList.remove("indicador-ocupado", "indicador-error");
            if (modo === "ocupado") {
                indicadorEstado.classList.add("indicador-ocupado");
            } else if (modo === "error") {
                indicadorEstado.classList.add("indicador-error");
            }
        }

        function agregarMensaje(rol, contenido, esError = false) {
            const div = document.createElement("div");
            div.classList.add("mensaje");

            if (esError) {
                div.classList.add("mensaje-error");
            } else if (rol === "usuario") {
                div.classList.add("mensaje-usuario");
            } else {
                div.classList.add("mensaje-asistente");
            }

            const small = document.createElement("small");
            small.textContent = rol === "usuario" ? "Tú" : (esError ? "Sistema" : "Tutor");

            const pre = document.createElement("pre");
            pre.textContent = contenido;

            div.appendChild(small);
            div.appendChild(pre);

            areaMensajes.appendChild(div);
            areaMensajes.scrollTop = areaMensajes.scrollHeight;
        }

        function limpiarChat() {
            mensajesAnteriores = [];
            areaMensajes.innerHTML = "";
            agregarMensaje(
                "asistente",
                "Empezamos un nuevo chat. Cuéntame qué tema quieres repasar hoy 🙂"
            );
            actualizarEstado("Listo para ayudarte.", "listo");
        }

        async function enviarMensaje() {
            const texto = entradaMensaje.value.trim();
            if (!texto) {
                return;
            }

            const materia = selectMateria.value.trim() || null;

            // Mostrar mensaje del usuario
            agregarMensaje("usuario", texto);
            entradaMensaje.value = "";
            actualizarEstado("Pensando la mejor forma de explicarlo...", "ocupado");
            botonEnviar.disabled = true;

            // Añadir al historial que se enviará al backend
            mensajesAnteriores.push({
                rol: "usuario",
                contenido: texto
            });

            // Recortar historial para no crecer infinito
            if (mensajesAnteriores.length > LIMITE_HISTORIAL) {
                mensajesAnteriores = mensajesAnteriores.slice(-LIMITE_HISTORIAL);
            }

            const cuerpo = {
                mensaje: texto,
                materia: materia,
                mensajes_anteriores: mensajesAnteriores
            };

            try {
                const respuesta = await fetch("/api/tutor", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(cuerpo)
                });

                if (!respuesta.ok) {
                    throw new Error("Error HTTP: " + respuesta.status);
                }

                const datos = await respuesta.json();
                const textoTutor = datos.respuesta || "(Sin respuesta)";

                agregarMensaje("asistente", textoTutor);

                // Añadir respuesta del asistente al historial
                mensajesAnteriores.push({
                    rol: "asistente",
                    contenido: textoTutor
                });
                if (mensajesAnteriores.length > LIMITE_HISTORIAL) {
                    mensajesAnteriores = mensajesAnteriores.slice(-LIMITE_HISTORIAL);
                }

                actualizarEstado("Listo para ayudarte.", "listo");
            } catch (error) {
                console.error(error);
                agregarMensaje(
                    "sistema",
                    "Ocurrió un error al comunicarme con el tutor. Verifica que el servidor esté en ejecución.",
                    true
                );
                actualizarEstado("Error al contactar con el tutor.", "error");
            } finally {
                botonEnviar.disabled = false;
            }
        }

        botonEnviar.addEventListener("click", enviarMensaje);

        entradaMensaje.addEventListener("keydown", function (evento) {
            if (evento.key === "Enter" && !evento.shiftKey) {
                evento.preventDefault();
                enviarMensaje();
            }
        });

        botonNuevoChat.addEventListener("click", function () {
            limpiarChat();
        });
    })();
</script>
</body>
</html>
    """
