from __future__ import annotations

from datetime import datetime
from uuid import UUID as UUIDType
from sqlalchemy import ForeignKey, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.db.enums import GameStatus

from .base_model import UUIDBase


class Game(UUIDBase):
    """
        Таблица игр.

        Колонки:
            - id:              уникальный идентификатор игры (UUID)
            - player1_id:      идентификатор первого игрока (UUID)
            - player2_id:      идентификатор второго игрока (UUID)
            - turn_player_id:  идентификатор игрока, чей сейчас ход (UUID)
            - winner_id:       идентификатор победителя игры (UUID)
            - status:          статус игры (Enum: WAITING, IN_PROGRESS, FINISHED)
            - started_at:      дата и время начала игры
            - finished_at:     дата и время окончания игры
            - created_at:      дата и время создания записи (из UUIDBase)
            - updated_at:      дата и время последнего обновления записи (из UUIDBase)

        Связи:
            - player1:         первый игрок (связь с таблицей игроков)
            - player2:         второй игрок (связь с таблицей игроков)
            - turn_player:     игрок, чей сейчас ход (связь с таблицей игроков)
            - winner:          победитель игры (связь с таблицей игроков)
    """

    __tablename__ = "games"

    player1_id:     Mapped[UUIDType] = mapped_column(UUID(as_uuid=True), ForeignKey("players.id"), nullable=False)
    player2_id:     Mapped[UUIDType] = mapped_column(UUID(as_uuid=True), ForeignKey("players.id"), nullable=False)

    turn_player_id: Mapped[UUIDType] = mapped_column(UUID(as_uuid=True), ForeignKey("players.id"))
    winner_id:      Mapped[UUIDType] = mapped_column(UUID(as_uuid=True), ForeignKey("players.id"))

    status:         Mapped[GameStatus] = mapped_column(Enum(GameStatus), default=GameStatus.WAITING, nullable=False, index=True)

    started_at:     Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    finished_at:    Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)

    player1:        Mapped["Player"] = relationship("Player", foreign_keys=[player1_id], back_populates="games_as_player1")
    player2:        Mapped["Player"] = relationship("Player", foreign_keys=[player2_id], back_populates="games_as_player2")
    turn_player:    Mapped["Player"] = relationship("Player", foreign_keys=[turn_player_id])
    winner:         Mapped["Player"] = relationship("Player", foreign_keys=[winner_id])

    game_boards = relationship("GameBoard", back_populates="game", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Game(sid={self.id}, status={self.status})>"


__all__ = [
    'Game'
]
