from pydantic import BaseModel
from typing import List, Literal


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


class GameBoard(BaseModel):
    """ Модель для представления игровой доски """

    board:           TGameBoardState
    shots_received:  TShotsRecord
    ships_remaining: int


class PlayerBoard(BaseModel):
    """ Модель для представления игровой доски игрока в ответе игры """

    player_id: str
    board:     GameBoard


__all__ = [
    'TGameBoardState',
    'TGameStateValue',
    'TShotsRecord',
    'GameBoard',
    'PlayerBoard'
]
