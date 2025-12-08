from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.api.rutas_chat import enrutador_chat
from app.api.rutas_sistema import enrutador_sistema
from app.api.rutas_interfaz import enrutador_interfaz
from app.api.rutas_conversaciones import enrutador_conversaciones
from app.security.dependencias import verificar_token_api


def crear_aplicacion() -> FastAPI:
    aplicacion = FastAPI(title="Tutor Local")

    origines_permitidos = ["*"]

    aplicacion.add_middleware(
        CORSMiddleware,
        allow_origins=origines_permitidos,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    aplicacion.include_router(enrutador_interfaz)

    aplicacion.include_router(
        enrutador_chat,
        prefix="/api",
        dependencies=[Depends(verificar_token_api)],
    )

    aplicacion.include_router(
        enrutador_sistema,
        prefix="/api",
        dependencies=[Depends(verificar_token_api)],
    )

    aplicacion.include_router(
        enrutador_conversaciones,
        prefix="/api",
        dependencies=[Depends(verificar_token_api)],
    )

    return aplicacion


app = crear_aplicacion()
