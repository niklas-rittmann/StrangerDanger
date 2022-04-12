from stranger_danger.db import session


async def test_context_session():
    """Test session context"""
    async with session.create_context_session() as sess:
        res = await sess.execute("SELECT 1")
    assert res.scalars().first()


async def test_create_session():
    """Test session context"""
    async for sess in session.create_session():
        res = await sess.execute("SELECT 1")
    assert res.scalars().first()
