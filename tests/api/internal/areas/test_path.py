from types import SimpleNamespace

import pytest
from fastapi.exceptions import HTTPException

from stranger_danger.api.app.internal.areas import path


def mock_db(return_value):
    class Db:
        async def execute(*args, **kwargs):
            return MockDb()

    class MockDb:
        @staticmethod
        def scalars():
            return MockDb()

        @staticmethod
        def first():
            return return_value

    return Db


async def test_dir_exists(monkeypatch):
    """Test if the given path is valid"""
    monkeypatch.setattr(path.os.path, "isdir", lambda _: False)
    with pytest.raises(HTTPException):
        await path.is_valid(3, "NotExisting")


async def test_path_already_used(monkeypatch):
    """Path already in use"""
    monkeypatch.setattr(path.os.path, "isdir", lambda _: True)
    with pytest.raises(HTTPException):
        await path.is_valid(mock_db(SimpleNamespace(id=3)), "Existing")


async def test_path_valid(monkeypatch):
    """Path valid and not in use"""

    monkeypatch.setattr(path.os.path, "isdir", lambda _: True)
    assert await path.is_valid(mock_db(False), "Existing")
