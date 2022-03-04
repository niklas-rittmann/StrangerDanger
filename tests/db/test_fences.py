import pytest

from stranger_danger.db.session import create_session
from stranger_danger.db.tables.fences import Fences
from stranger_danger.fences.circular_fence import CircularFence
from stranger_danger.fences.protocol import Coordinate


@pytest.mark.asyncio
async def test_upload_fence():
    """Upload a circular fence to the databse"""
    circ = CircularFence(name="Testfence", center=Coordinate(x=1, y=2), radius=3)
    fence = Fences(id=-1, definition=circ.schema_json())
    async for sess in create_session():
        sess.add(fence)
