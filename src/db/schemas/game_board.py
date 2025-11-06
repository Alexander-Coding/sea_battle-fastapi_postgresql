from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, field_serializer
from typing import List, Literal, Optional


"""
Типы для представления состояния игровой доски
    0     - пустая клетка 
    1 - 4 - клетка с кораблем (число обозначает размер корабля)
    -1    - промах
    -2    - попадание
"""
TGameStateValue = int
TGameBoardState = List[List[TGameStateValue]]


"""
Тип для представления выстрелов по игровой доске
    True  - выстрел произведен
    False - выстрел не произведен
"""
TShotsRecord = List[List[bool]]


class GameBoardSchema(BaseModel):
    """ Схема модели игровой доски """

    id:              UUID
    game_id:         UUID
    player_id:       UUID
    board_state:     TGameBoardState
    shots_record:    TShotsRecord
    created_at:      datetime
    updated_at:      Optional[datetime]
    ships_remaining: int

    class Config:
        from_attributes = True

    @field_serializer('id', 'game_id', 'player_id')
    def _serialize_uuid(self, value: UUID | None) -> UUID | None:
        if value is None:
            return None

        return str(value)


class GameBoardViewSchema(BaseModel):
    """ Модель для представления игровой доски """

    board:           TGameBoardState
    shots_received:  TShotsRecord
    ships_remaining: int


class PlayerBoardSchema(BaseModel):
    """ Модель для представления игровой доски игрока в ответе игры """

    player_id: UUID
    board:     GameBoardViewSchema

    @field_serializer('player_id')
    def _serialize_uuid(self, value: UUID | None) -> UUID | None:
        if value is None:
            return None

        return str(value)


__all__ = [
    'TGameBoardState',
    'TGameStateValue',
    'TShotsRecord',
    'GameBoardViewSchema',
    'PlayerBoardSchema',
    'GameBoardSchema'
]
