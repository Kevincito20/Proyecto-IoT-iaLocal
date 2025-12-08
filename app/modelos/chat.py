from pydantic import BaseModel


class PeticionChat(BaseModel):
    """
    Representa la petición de chat enviada por el cliente.
    El campo mensaje puede incluir historial resumido + mensaje actual.
    """

    mensaje: str
