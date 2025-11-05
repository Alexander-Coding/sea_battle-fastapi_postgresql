from enum import Enum
from typing import Optional
from pydantic import BaseModel

from src.db.schemas import TGameBoardState, TShotsRecord


class WSMessageType(str, Enum):
    START_GAME = "start_game"
    MOVE = "move"
    GAME_STATE = "game_state"
    GAME_OVER = "game_over"
    ERROR = "error"
    CONNECTED = "connected"


class MoveMessage(BaseModel):
    x: int
    y: int


class GameStateMessage(BaseModel):
    game_id:         str
    turn_player_id:  str
    your_board:      TGameBoardState
    opponent_shots:  TShotsRecord
    your_shots:      TShotsRecord
    ships_remaining: int
    opponent_ships_remaining: int


class WSMessage(BaseModel):
    type:    WSMessageType
    data:    Optional[dict] = None
    message: Optional[str] = None


__all__ = [
    'WSMessageType',
    'MoveMessage',
    'GameStateMessage',
    'WSMessage'
]
