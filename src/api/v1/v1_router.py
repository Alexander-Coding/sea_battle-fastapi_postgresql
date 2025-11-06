from fastapi import APIRouter

from .players import api_players_router
from .games import api_game_router
from .websocket import ws_router


v1_router = APIRouter(prefix='/v1', tags=['v1'])
v1_router.include_router(api_players_router, prefix='/players', tags=['players'])
v1_router.include_router(api_game_router, prefix='/games', tags=['games'])
v1_router.include_router(ws_router, prefix='/games', tags=['ws'])


__all__ = [
    'v1_router',
]

