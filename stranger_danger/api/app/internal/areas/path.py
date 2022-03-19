import os

from fastapi import HTTPException
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql.expression import select

from stranger_danger.db.tables.areas import Areas


async def is_valid(db: AsyncSession, watch_dir: str) -> bool:
    """Check if directory is a valid and doesnt exist"""
    if not os.path.isdir(watch_dir):
        raise HTTPException(status_code=404, detail=f"Not a directory: {watch_dir}")
    areas = await db.execute(select(Areas).where(Areas.directory == watch_dir))
    if area := areas.scalars().first():
        raise HTTPException(
            status_code=404,
            detail=f"Area already exists with area id:{area.id}",
        )
    return True
