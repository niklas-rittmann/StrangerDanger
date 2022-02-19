import pytest
from pydantic import ValidationError

from stranger_danger.fences.protocol import Coordinate, Fence
from stranger_danger.fences.rectangular_fence import RectangularFence


@pytest.fixture
def rec() -> Fence:
    return RectangularFence(
        name="Test Fence",
        coordinates=(Coordinate(x=2, y=3), Coordinate(x=0, y=0)),
    )


def test_validation_error():
    """Test whether the input validation works"""

    with pytest.raises(ValidationError):
        RectangularFence(center=4, radius=1)

    with pytest.raises(ValidationError):
        RectangularFence(center=(3, 3), radius=(1,))


def test_attributes(rec):
    """Test if argument assinment works"""
    assert rec.name == "Test Fence"
    assert rec.coordinates[0].x == 2
    assert rec.coordinates[0].y == 3
    assert rec.coordinates[1].x == 0
    assert rec.coordinates[1].y == 0


def test_inside_func(rec):
    """Test if a point inside the recle is recognised"""
    assert rec.inside_fence(Coordinate(x=1, y=1))


def test_outside_func(rec):
    """Test if a point outside the recle is recognised"""
    assert not rec.inside_fence(Coordinate(x=3, y=4))
