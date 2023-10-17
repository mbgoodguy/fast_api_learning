from datetime import datetime
from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy import String, Boolean, Integer, ForeignKey, TIMESTAMP, Column
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, DeclarativeMeta, declarative_base, Mapped, mapped_column

from config import DB_USER, DB_HOST, DB_NAME, DB_PASS, DB_PORT
from models.models import role

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


class Base(DeclarativeBase):
    pass


class User(SQLAlchemyBaseUserTable[int], Base):
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    username = Column(String, nullable=False)
    registred_at = Column(TIMESTAMP, default=datetime.utcnow)
    hashed_password = Column(String, nullable=False)
    role_id = Integer, ForeignKey(role.c.id)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)

    engine = create_async_engine(DATABASE_URL)
    async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


engine = create_async_engine(DATABASE_URL)  # engine - Точка входа алхимии в наше приложение. С помощью движка создаем
# сессии (временные соединения) чтобы можно было работать с БД (удалять данные, обновить)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
