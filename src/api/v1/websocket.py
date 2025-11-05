import json

from typing import Dict
from datetime import datetime
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.repositories import (
    PlayerRepository,
    GameRepository,
    GameBoardRepository
)

from src.core import database_client
from src.db.enums import GameStatus
from src.db.models import Player, Game, GameBoard
from src.schemas.websocket import WSMessageType, MoveMessage, GameStateMessage
from src.services.game_logic import process_move, check_winner
from src.utils import SingletonMeta
from src import logger

ws_router = APIRouter()

# Активные WebSocket соединения {game_id: {player_id: websocket}}
active_connections: Dict[str, Dict[str, WebSocket]] = {}


class ConnectionManager(metaclass=SingletonMeta):
    def __init__(self):
        self.active_connections: Dict[str, Dict[str, WebSocket]] = {}

    async def connect(self, websocket: WebSocket, game_id: str, player_id: str):
        await websocket.accept()

        if game_id not in self.active_connections:
            self.active_connections[game_id] = {}

        self.active_connections[game_id][player_id] = websocket
        logger.info(f"Игрок {player_id} подключен к игре {game_id}")

    def disconnect(self, game_id: str, player_id: str):
        if game_id in self.active_connections:
            if player_id in self.active_connections[game_id]:
                del self.active_connections[game_id][player_id]
                logger.info(f"Игрок {player_id} отключен от игры {game_id}")

            if not self.active_connections[game_id]:
                del self.active_connections[game_id]

    async def send_personal_message(self, message: dict, game_id: str, player_id: str):
        if game_id in self.active_connections and player_id in self.active_connections[game_id]:
            websocket = self.active_connections[game_id][player_id]
            await websocket.send_json(message)

    async def broadcast_to_game(self, message: dict, game_id: str):
        if game_id in self.active_connections:
            for player_sid, websocket in self.active_connections[game_id].items():
                await websocket.send_json(message)


manager = ConnectionManager()


@ws_router.websocket("/{game_sid}/play")
async def websocket_endpoint(websocket: WebSocket, game_id: str, token: str):
    """WebSocket для игры"""
    db = database_client.async_session_factory()

    player_id = None

    try:
        # Проверка токена и получение игрока
        from src.services.auth import decode_access_token

        payload = decode_access_token(token)
        player_id = payload.get("sub")

        if not player_id:
            await websocket.close(code=1008)
            return

        players_repo = PlayerRepository(session=db)
        player = await players_repo.get_one_or_none(Player.id == player_id)

        if not player:
            await websocket.close(code=1008)
            return

        # Проверка игры
        game_repo = GameRepository(session=db)
        game = await game_repo.get_one_or_none(Game.id == game_id)

        if not game:
            await websocket.close(code=1008)
            return

        # Проверка, что игрок участвует в игре
        if game.player1_id != player.id and game.player2_id != player.id:
            await websocket.close(code=1008)
            return

        # Подключение
        await manager.connect(websocket, game_id, player_id)

        # Отправка подтверждения подключения
        await manager.send_personal_message(
            {
                "type": WSMessageType.CONNECTED,
                "message": f"Подключено к игре {game_id}"
            },
            game_id,
            player_id
        )

        # Обработка сообщений
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)

            msg_type = message.get("type")

            if msg_type == WSMessageType.START_GAME:
                # Начало игры
                logger.info(f"Начата игра {game_id}")

                game.status = GameStatus.IN_PROGRESS
                game.started_at = datetime.now()
                await db.commit()

                await manager.broadcast_to_game(
                    {
                        "type": WSMessageType.GAME_STATE,
                        "message": "Игра начата!"
                    },
                    game_id
                )

                # Отправка состояния игры обоим игрокам
                await send_game_state(db, game, manager)

            elif msg_type == WSMessageType.MOVE:
                # Обработка хода
                if game.status != GameStatus.IN_PROGRESS:
                    await manager.send_personal_message(
                        {
                            "type": WSMessageType.ERROR,
                            "message": "Игра не в процессе"
                        },
                        game_id,
                        player_id
                    )
                    continue

                # Проверка, чей ход
                if game.current_turn_player_id != player.id:
                    await manager.send_personal_message(
                        {
                            "type": WSMessageType.ERROR,
                            "message": "Не ваш ход"
                        },
                        game_id,
                        player_id
                    )
                    continue

                move_data = MoveMessage(**message.get("data", {}))

                # Обработка хода
                opponent_id = game.player2_id if game.player1_id == player.id else game.player1_id

                hit, sunk = await process_move(db, game, move_data.x, move_data.y, opponent_id)

                # Проверка победителя
                winner_id = await check_winner(db, game)

                if winner_id:
                    game.winner_id = winner_id
                    game.status = GameStatus.FINISHED
                    game.finished_at = datetime.now()
                    await db.commit()

                    winner_sid = game.player1.sid if winner_id == game.player1_id else game.player2.sid

                    await manager.broadcast_to_game(
                        {
                            "type": WSMessageType.GAME_OVER,
                            "data": {
                                "winner_id": winner_sid,
                                "message": f"Игрок {winner_sid} победил!"
                            }
                        },
                        game_id
                    )

                    logger.info(f"Игра {game_id} Завершена. Победитель: {winner_sid}")
                else:
                    # Смена хода, если промах
                    if not hit:
                        game.current_turn_player_id = opponent_id
                        await db.commit()

                    # Отправка обновленного состояния
                    await send_game_state(db, game, manager)

    except WebSocketDisconnect:
        manager.disconnect(game_id, player_id)
        logger.info(f"Игрок {player_id} отключен от игры {game_id}")

    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(game_id, player_id)

    finally:
        await db.close()


async def send_game_state(db: AsyncSession, game: Game, manager: ConnectionManager):
    """Отправка текущего состояния игры всем игрокам"""

    # Получение досок
    game_board_repo = GameBoardRepository(session=db)
    boards = await game_board_repo.list(GameBoard.game_id == game.id)

    for board in boards:
        player_id = game.player1.sid if board.player_id == game.player1_id else game.player2.sid
        opponent_board = next(b for b in boards if b.player_id != board.player_id)

        # Создание состояния игры для игрока
        state = GameStateMessage(
            game_id=game.id,
            turn_player_id=game.player1.sid if game.turn_player_id == game.player1_id else game.player2.sid,
            your_board=board.board_state,
            opponent_shots=board.shots_record,
            your_shots=opponent_board.shots_record,
            ships_remaining=board.ships_remaining,
            opponent_ships_remaining=opponent_board.ships_remaining
        )

        await manager.send_personal_message(
            {
                "type": WSMessageType.GAME_STATE,
                "data": state.model_dump()
            },
            game.id,
            player_id
        )


__all__ = [
    'ws_router'
]
