from pydantic import BaseModel

from src.db.schemas import PlayerResponseSchema


class TokenSchema(BaseModel):
    """ Модель для представления токена аутентификации """

    access_token: str
    token_type:   str = "bearer"
    player:       PlayerResponseSchema


__all__ = [
    'TokenSchema'
]
