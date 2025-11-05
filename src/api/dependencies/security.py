from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src import logger
from src.core import database_client
from src.db.models import Player
from src.services.auth import decode_access_token


security = HTTPBearer()


async def get_current_player(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db:          AsyncSession = Depends(database_client.get_session)
) -> Player:
    """Получение текущего аутентифицированного игрока"""
    try:
        token = credentials.credentials
        payload = decode_access_token(token)
        player_id = payload.get("sub", None)

        if player_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Недействительный токен"
            )

        result = await db.execute(select(Player).where(Player.id == player_id))
        player = result.scalar_one_or_none()

        if player is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Игрок не найден"
            )

        return player

    except Exception as e:
        logger.error(f"Authentication error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Ошибка аутентификации"
        )


__all__ = [
    'get_current_player',
]
