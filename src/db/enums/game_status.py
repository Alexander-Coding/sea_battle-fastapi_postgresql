from enum import Enum


class GameStatus(str, Enum):
    """ Перечисление статусов игры. """

    WAITING = "waiting"
    IN_PROGRESS = "in_progress"
    FINISHED = "finished"


__all__ = [
    'GameStatus'
]
