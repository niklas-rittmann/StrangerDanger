import asyncio
from typing import AsyncIterable

import pytest
from sqlalchemy.ext.asyncio.session import AsyncSession

from stranger_danger.db.session import create_session


@pytest.fixture(scope="session")
def sess():
    yield create_session()


@pytest.mark.asyncio
async def test_db_connection(sess: AsyncIterable[AsyncSession]):
    """Check if the databse connection works"""

    async for session in sess:
        print(await session.execute("SELECT 1"))
