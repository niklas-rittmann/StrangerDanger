import asyncio
from typing import Tuple

import pytest
from pydantic import ValidationError

from stranger_danger.fences.pentagon_fence import PentagonFence, _inside_pentagon
from stranger_danger.fences.protocol import Coordinate, Fence


@pytest.fixture
def pent() -> Fence:

    coordinates = (
        Coordinate(x=0, y=0),
        Coordinate(x=3, y=0),
        Coordinate(x=3, y=3),
        Coordinate(x=1, y=4),
        Coordinate(x=0, y=3),
    )
    return PentagonFence(name="Test Fence", coordinates=coordinates)


def test_validation_error():
    """Test whether the input validation works"""

    with pytest.raises(ValidationError):
        PentagonFence(coordinates=(3, 3))

    with pytest.raises(ValidationError):
        PentagonFence(coordinates=(Coordinate(x=3, y=4)))


def test_attributes(pent):
    """Test if argument assinment works"""
    assert pent.name == "Test Fence"
    assert pent.coordinates[2].x == 3
    assert pent.coordinates[3].y == 4


def test_inside_func(pent):
    """Test if a point inside the pentle is recognised"""
    assert asyncio.run(pent.inside_fence(Coordinate(x=1, y=1)))


def test_outside_func(pent):
    """Test if a point outside the pentle is recognised"""
    assert not asyncio.run(pent.inside_fence(Coordinate(x=4, y=5)))


@pytest.mark.parametrize(
    "point, expected", [((0, 3), True), ((0, 0), True), ((4, 0), False)]
)
def test_inside_pentagon(pent, point: Tuple, expected: bool):
    """Test if the underlying pentagon function works"""
    coordinates = pent.coordinates
    assert _inside_pentagon(coordinates, Coordinate(x=point[0], y=point[1])) == expected
