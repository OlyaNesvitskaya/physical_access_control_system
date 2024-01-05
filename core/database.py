from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from core.environment import settings

async_engine = create_async_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False}, echo=True)

async_session = async_sessionmaker(async_engine, expire_on_commit=False)


async def get_db_connection() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session







