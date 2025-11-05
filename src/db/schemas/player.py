from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional, Literal


TGameResult = Literal["win", "loss"]


class PlayerCreate(BaseModel):
    """ Модель для создания игрока """

    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)


class PlayerLogin(BaseModel):
    """ Модель для входа игрока """

    username: str
    password: str


class PlayerResponse(BaseModel):
    """ Модель ответа с информацией об игроке """

    id:         str
    username:   str
    created_at: datetime

    class Config:
        from_attributes = True


class GameResult(BaseModel):
    """ Модель для представления результата игры """

    game_id:           str
    opponent_username: str
    result:            TGameResult
    created_at:        datetime
    finished_at:       Optional[datetime]


class PlayerStats(BaseModel):
    """ Модель для представления статистики игрока """

    player:      PlayerResponse
    total_games: int
    wins:        int
    losses:      int
    games:       List[GameResult]


__all__ = [
    'PlayerCreate',
    'PlayerLogin',
    'PlayerResponse',
    'GameResult',
    'PlayerStats'
]
