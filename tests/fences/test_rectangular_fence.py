import asyncio

import pytest
from pydantic import ValidationError

from stranger_danger.fences.protocol import Coordinate, Fence
from stranger_danger.fences.rectangular_fence import RectangularFence, _between_points


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
    assert asyncio.run(rec.inside_fence(Coordinate(x=1, y=1)))


def test_outside_func(rec):
    """Test if a point outside the recle is recognised"""
    assert not asyncio.run(rec.inside_fence(Coordinate(x=3, y=4)))


def test_point_in_between_points():
    """Test if a point inside to other points is detected"""
    lower, upper = (0, 5)
    valid_target = 3
    invalid_target = 6

    assert _between_points(lower, upper, valid_target)
    assert not _between_points(lower, upper, invalid_target)


def test_between_points_mixed_order():
    """Test if a point inside to other points is detected with switched input"""
    lower, upper = (5, 0)
    valid_target = 3
    invalid_target = 6

    assert _between_points(lower, upper, valid_target)
    assert not _between_points(lower, upper, invalid_target)


def test_draw_fence(rec: RectangularFence):
    """Test if the fence is drawn into an empty image"""
    image = asyncio.run(rec.draw_fence())
    assert tuple(image[0, 0, :]) != (0, 0, 0)
    assert tuple(image[100, 100, :]) == (0, 0, 0)
