from types import SimpleNamespace

import pytest
from fastapi.exceptions import HTTPException

from stranger_danger.api.app.internal.areas import path
from stranger_danger.api.app.internal.areas.schema import AreaBase
from stranger_danger.db.tables.areas import Areas


def mock_db(return_value):
    class Db:
        async def execute(*args, **kwargs):
            return MockDb()

        @staticmethod
        def add(*args):
            return None

        @staticmethod
        async def flush():
            return Areas(id=4, directory="dir")

    class MockDb:
        @staticmethod
        def scalars():
            return MockDb()

        @staticmethod
        def first():
            return return_value

    return Db


async def raiseHttpException(*args, **kwargs):
    raise HTTPException(status_code=200)


async def valid(*args, **kwargs):
    return True


def area(*args, **kwargs):
    return AreaBase(id=3, status="created")


async def test_path_not_valid(monkeypatch):
    """Test validation failed"""
    monkeypatch.setattr(path, "is_valid", raiseHttpException)
    with pytest.raises(HTTPException):
        await path.check_store_area(3, "dir")


async def test_check_and_stor(monkeypatch):
    """Test store area in db"""
    monkeypatch.setattr(path, "is_valid", valid)
    monkeypatch.setattr(path, "Areas", area)
    return_area = await path.check_store_area(mock_db(True), "dir")
    assert return_area.id == 3


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
