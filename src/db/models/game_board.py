from __future__ import annotations

from datetime import datetime
from uuid import UUID as UUIDType
from sqlalchemy import ForeignKey, Index, Integer
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.db.schemas import TShotsRecord, TGameBoardState

from .base_model import UUIDBase


class GameBoard(UUIDBase):
    """
        Таблица игровой доски.

        Колонки:
            - id:              уникальный идентификатор игровой доски (UUID)
            - game_id:         идентификатор игры (UUID)
            - player_id:       идентификатор игрока (UUID)
            - board_state:     состояние игровой доски (JSONB)
            - shots_record:    запись выстрелов (JSONB)
            - ships_remaining: количество оставшихся кораблей у игрока (Integer)
            - created_at:      дата и время создания записи (из UUIDBase)
            - updated_at:      дата и время последнего обновления записи (из UUIDBase)

        Связи:
            - game:            игра, связанная с игровой доской
            - player:          игрок, связанный с игровой доской

        Индексы:
            - ix_game_boards_game_id_player_id: уникальный индекс по колонкам game_id
                и player_id для обеспечения уникальности игровой доски на игрока в игре

            - idx_game_boards_board_state: GIN-индекс по колонке board_state для
                оптимизации запросов, связанных с состоянием игровой доски

            - idx_game_boards_shots_record: GIN-индекс по колонке shots_record для
                оптимизации запросов, связанных с записью выстрелов
    """

    __tablename__ = "game_boards"

    game_id:         Mapped[UUIDType] = mapped_column(UUID(as_uuid=True), ForeignKey("games.id"), nullable=False)
    player_id:       Mapped[UUIDType] = mapped_column(UUID(as_uuid=True), ForeignKey("players.id"), nullable=False)

    board_state:     Mapped[TGameBoardState] = mapped_column(JSONB, nullable=False)
    shots_record:    Mapped[TShotsRecord] = mapped_column(JSONB, nullable=False)
    ships_remaining: Mapped[int] = mapped_column(Integer, default=10, nullable=False)

    game:   Mapped["Game"] = relationship("Game", back_populates="game_boards")
    player: Mapped["Game"] = relationship("Player", back_populates="game_boards")

    __table_args__ = (
        Index('ix_game_boards_game_id_player_id', 'game_id', 'player_id', unique=True),
        Index('idx_game_boards_board_state', 'board_state', postgresql_using='gin'),
        Index('idx_game_boards_shots_record', 'shots_record', postgresql_using='gin'),
    )

    def __repr__(self):
        return f"<GameBoard(game_id={self.game_id}, player_id={self.player_id})>"


__all__ = [
    'GameBoard'
]
