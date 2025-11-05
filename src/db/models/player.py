from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import relationship, Mapped, mapped_column

from .base_model import UUIDBase


class Player(UUIDBase):
    """
        Таблица игроков.

        Колонки:
            - id:              уникальный идентификатор игрока (UUID)
            - username:        уникальное имя пользователя
            - hashed_password: хешированный пароль пользователя
            - created_at:      дата и время создания записи (из UUIDBase)
            - updated_at:      дата и время последнего обновления записи (из UUIDBase)

        Связи:
            - games_as_player1: игры, в которых игрок выступает как первый игрок
            - games_as_player2: игры, в которых игрок выступает как второй игрок
            - game_boards:      игровые доски, связанные с игроком
    """

    __tablename__ = "players"

    username:         Mapped[str] = mapped_column(String(128), unique=True, index=True, nullable=False)
    hashed_password:  Mapped[str] = mapped_column(String(128), nullable=False)

    games_as_player1: Mapped["Game"] = relationship("Game", foreign_keys="Game.player1_id", back_populates="player1")
    games_as_player2: Mapped["Game"] = relationship("Game", foreign_keys="Game.player2_id", back_populates="player2")
    game_boards:      Mapped["GameBoard"] = relationship("GameBoard", back_populates="player", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Player(sid={self.id}, username={self.username})>"


__all__ = [
    'Player'
]
