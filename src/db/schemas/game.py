from __future__ import annotations

from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, field_serializer
from typing import List, Optional

from src.db.enums import GameStatus
from src.db.schemas import PlayerBoardSchema, GameBoardSchema


class GameSchema(BaseModel):
    """ Схема модели игры """

    id:             UUID
    player1_id:     UUID
    player2_id:     UUID
    turn_player_id: Optional[UUID]
    winner_id:      Optional[UUID]
    status:         GameStatus
    created_at:     datetime
    started_at:     Optional[datetime]
    finished_at:    Optional[datetime]
    updated_at:     Optional[datetime]

    class Config:
        from_attributes = True

    @field_serializer('id', 'player1_id', 'player2_id', 'turn_player_id', 'winner_id')
    def _serialize_uuid(self, value: UUID | None) -> UUID | None:
        if value is None:
            return None

        return str(value)


class GameCreateSchema(BaseModel):
    """ Модель для создания игры """

    player1_id: UUID
    player2_id: UUID

    @field_serializer('player1_id', 'player2_id')
    def _serialize_uuid(self, value: UUID | None) -> UUID | None:
        if value is None:
            return None

        return str(value)


class GameResponseSchema(BaseModel):
    """ Модель ответа с информацией об игре """

    id:             UUID
    player1_id:     UUID
    player2_id:     UUID
    turn_player_id: Optional[UUID] = None
    winner_id:      Optional[UUID] = None
    status:         GameStatus
    created_at:     datetime
    started_at:     Optional[datetime] = None
    finished_at:    Optional[datetime] = None
    boards:         List[PlayerBoardSchema]

    class Config:
        from_attributes = True

    @field_serializer('id', 'player1_id', 'player2_id', 'turn_player_id', 'winner_id')
    def _serialize_uuid(self, value: UUID | None) -> UUID | None:
        if value is None:
            return None

        return str(value)


class GameStatsSchema(BaseModel):
    id:               UUID
    player1_username: str
    player2_username: str
    winner_username:  Optional[str]
    status:           GameStatus
    created_at:       datetime
    finished_at:      Optional[datetime]

    @field_serializer('id')
    def _serialize_uuid(self, value: UUID | None) -> UUID | None:
        if value is None:
            return None

        return str(value)


__all__ = [
    'GameSchema',
    'GameCreateSchema',
    'GameResponseSchema',
    'GameStatsSchema'
]
