import asyncio

import pytest
from pydantic import ValidationError

from stranger_danger.fences.circular_fence import CircularFence, _square_root_distance
from stranger_danger.fences.protocol import Coordinate, Fence


@pytest.fixture
def circ() -> Fence:
    return CircularFence(name="Test Fence", center=Coordinate(x=2, y=3), radius=1)


def test_validation_error():
    """Test whether the input validation works"""

    with pytest.raises(ValidationError):
        CircularFence(center=4, radius=1)

    with pytest.raises(ValidationError):
        CircularFence(center=(3, 3), radius=(1,))


def test_attributes(circ):
    """Test if argument assinment works"""
    assert circ.name == "Test Fence"
    assert circ.center.x == 2
    assert circ.center.y == 3


def test_inside_func(circ):
    """Test if a point inside the circle is recognised"""
    assert asyncio.run(circ.inside_fence(Coordinate(x=3, y=3)))


def test_outside_func(circ):
    """Test if a point outside the circle is recognised"""
    assert not asyncio.run(circ.inside_fence(Coordinate(x=4, y=5)))


def test_square_root_dist():
    """Test if the square root calculation works as expected"""
    base = Coordinate(x=0, y=0)
    target = Coordinate(x=3, y=4)
    assert _square_root_distance(base, target) == 5
