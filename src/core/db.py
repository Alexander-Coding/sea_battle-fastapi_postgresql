from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Optional, AsyncGenerator, Any
from sqlalchemy.pool import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine, async_sessionmaker
from advanced_alchemy.config import AsyncSessionConfig, SQLAlchemyAsyncConfig

from src import config
from src.utils import SingletonMeta


class DatabaseClient(metaclass=SingletonMeta):
    """Класс для работы с PostgresSQL базой данных"""

    def __init__(self):
        self._engine:                Optional[AsyncEngine] = None
        self._async_session_factory: Optional[async_sessionmaker] = None
        self._sqlalchemy_config:     Optional[SQLAlchemyAsyncConfig] = None

    @property
    def engine(self) -> AsyncEngine:
        if not self._engine:
            self.initialize()

        return self._engine

    @property
    def async_session_factory(self) -> async_sessionmaker:
        if not self._async_session_factory:
            self.initialize()

        return self._async_session_factory

    @property
    def sqlalchemy_config(self) -> SQLAlchemyAsyncConfig:
        if not self._sqlalchemy_config:
            self.initialize()

        return self._sqlalchemy_config

    async def initialize(self):
        """
        Инициализация подключения к базе данных
        """

        self._engine = create_async_engine(
            config.database_url,
            echo=False,
            poolclass=NullPool,
            pool_pre_ping=True
        )

        self._async_session_factory = async_sessionmaker(
            bind=self._engine,
            expire_on_commit=False,
            autoflush=False,
            class_=AsyncSession
        )

        session_config = AsyncSessionConfig(
            expire_on_commit=False,
            autoflush=False
        )

        self._sqlalchemy_config = SQLAlchemyAsyncConfig(
            connection_string=config.database_url,
            session_config=session_config
        )

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Получение сессии базы данных"""
        if not self._engine:
            await self.initialize()

        async with self.async_session_factory() as session:
            yield session

            await session.commit()

    async def get_db(self) -> AsyncGenerator[AsyncSession | Any, Any]:
        if not self._engine:
            await self.initialize()

        async with self.async_session_factory() as db:
            yield db

            await db.commit()
            await db.close()

    async def create_tables(self):
        """
        Создание таблиц
        """

        if not self._engine:
            await self.initialize()

        from src.db.models import UUIDBase

        async with self._engine.begin() as conn:
            await conn.run_sync(UUIDBase.metadata.create_all)

    async def stop(self):
        """
        Закрытие подключения к базе данных
        """

        if self._engine:
            await self._engine.dispose()


database_client = DatabaseClient()


__all__ = [
    'database_client'
]
