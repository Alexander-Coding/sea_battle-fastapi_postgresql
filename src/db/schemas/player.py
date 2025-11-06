from __future__ import annotations

from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field, field_serializer
from typing import List, Optional, Literal


TGameResult = Literal["win", "loss"]


class PlayerSchema(BaseModel):
    """ Схема модели игрока """

    id:         UUID
    username:   str
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

    @field_serializer('id')
    def _serialize_uuid(self, value: UUID | None) -> UUID | None:
        if value is None:
            return None

        return str(value)


class PlayerCreateSchema(BaseModel):
    """ Модель для создания игрока """

    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)


class PlayerLoginSchema(BaseModel):
    """ Модель для входа игрока """

    username: str
    password: str


class PlayerResponseSchema(BaseModel):
    """ Модель ответа с информацией об игроке """

    id:         UUID
    username:   str
    created_at: datetime

    class Config:
        from_attributes = True

    @field_serializer('id')
    def _serialize_uuid(self, value: UUID | None) -> UUID | None:
        if value is None:
            return None

        return str(value)


class GameResultSchema(BaseModel):
    """ Модель для представления результата игры """

    game_id:           UUID
    opponent_username: str
    result:            TGameResult
    created_at:        datetime
    finished_at:       Optional[datetime]

    @field_serializer('game_id')
    def _serialize_uuid(self, value: UUID | None) -> UUID | None:
        if value is None:
            return None

        return str(value)


class PlayerStatsSchema(BaseModel):
    """ Модель для представления статистики игрока """

    player:      PlayerResponseSchema
    total_games: int
    wins:        int
    losses:      int
    games:       List[GameResultSchema]


__all__ = [
    'PlayerCreateSchema',
    'PlayerLoginSchema',
    'PlayerResponseSchema',
    'GameResultSchema',
    'PlayerStatsSchema',
    'PlayerSchema'
]
