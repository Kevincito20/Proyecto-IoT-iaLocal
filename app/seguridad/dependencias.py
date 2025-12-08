from fastapi import Header, HTTPException, status

from app.configuracion.ajustes import ajustes


async def verificar_token_api(x_token_api: str = Header(...)) -> None:
    """
    Verifica que el encabezado X-Token-Api coincida con el token configurado.
    """
    if not ajustes.token_api:
        return

    if x_token_api != ajustes.token_api:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de acceso inválido",
        )
