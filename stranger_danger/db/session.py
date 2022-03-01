import asyncio
from typing import AsyncIterable

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from stranger_danger.db.config.settings import DB_URL

engine = create_async_engine(DB_URL, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def create_session() -> AsyncIterable[AsyncSession]:
    """Yield a databse session"""
    async with async_session() as session:
        yield session
        await session.commit()
    await engine.dispose()
