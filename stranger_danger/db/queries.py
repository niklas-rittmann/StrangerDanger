from sqlalchemy.ext.asyncio.session import AsyncSession

from stranger_danger.db.config.settings import Base


async def get_by_id(db: AsyncSession, table: Base, id: int) -> Base:
    """Return db entry by id"""
    return await db.get(table, id)
