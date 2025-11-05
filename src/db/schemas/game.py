from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional

from src.db.enums import GameStatus
from src.db.schemas import PlayerBoard, GameBoard


class GameCreate(BaseModel):
    """ Модель для создания игры """

    player1_id: str
    player2_id: str


class GameResponse(BaseModel):
    """ Модель ответа с информацией об игре """

    id:             str
    player1_id:     str
    player2_id:     str
    turn_player_id: Optional[str] = None
    winner_id:      Optional[str] = None
    status:         GameStatus
    created_at:     datetime
    started_at:     Optional[datetime] = None
    finished_at:    Optional[datetime] = None
    boards:         List[PlayerBoard]

    class Config:
        from_attributes = True


class GameStats(BaseModel):
    sid:              str
    player1_username: str
    player2_username: str
    winner_username:  Optional[str]
    status:           GameStatus
    created_at:       datetime
    finished_at:      Optional[datetime]


__all__ = [
    'GameCreate',
    'GameResponse',
    'GameStats'
]
