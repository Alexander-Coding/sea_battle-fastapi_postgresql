from datetime import datetime
from pydantic import BaseModel
from typing import List, Literal, Optional


"""
Типы для представления состояния игровой доски
    0     - пустая клетка 
    1 - 4 - клетка с кораблем (число обозначает размер корабля)
    -1    - промах
    -2    - попадание
"""
TGameStateValue = Literal[0, 1, 2, 3, 4, -1, -2]
TGameBoardState = List[List[TGameStateValue]]


"""
Тип для представления выстрелов по игровой доске
    True  - выстрел произведен
    False - выстрел не произведен
"""
TShotsRecord = List[List[bool]]


class GameBoardSchema(BaseModel):
    """ Схема модели игровой доски """

    id:           str
    game_id:      str
    player_id:    str
    board_state:  TGameBoardState
    shots_record: TShotsRecord
    created_at:   datetime
    updated_at:   Optional[datetime]

    class Config:
        from_attributes = True


class GameBoardViewSchema(BaseModel):
    """ Модель для представления игровой доски """

    board:           TGameBoardState
    shots_received:  TShotsRecord
    ships_remaining: int


class PlayerBoardSchema(BaseModel):
    """ Модель для представления игровой доски игрока в ответе игры """

    player_id: str
    board:     GameBoardViewSchema


__all__ = [
    'TGameBoardState',
    'TGameStateValue',
    'TShotsRecord',
    'GameBoardViewSchema',
    'PlayerBoardSchema',
    'GameBoardSchema'
]
