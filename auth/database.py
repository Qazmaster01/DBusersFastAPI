from typing import AsyncGenerator
from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, declarative_base
from config import DB_HOST, DB_PORT, DB_USER, DB_NAME, DB_PASS
from sqlalchemy import Column, String, Boolean

DATABASE_URL = f"postgresql+aiosqlite://%{DB_USER}s:%{DB_PASS}s@%{DB_HOST}s:%{DB_PORT}s/%{DB_NAME}s"
Base: DeclarativeMeta = declarative_base()
class User(SQLAlchemyBaseUserTable[int], Base):
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    email: str = Column(String(length=320), unique=True, index=True, nullable=False)
    hashed_password: str = Column(String(length=1024), nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    us_verifed: bool = Column(Boolean, default=False, nullable=False)

#точка входа sqlalcheny для нашего приложения
engine = create_async_engine(DATABASE_URL)
#временные сессий
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

#получение асинх сессий
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)