import pytest
from pydantic import ValidationError

from stranger_danger.fences.circular_fence import CircularFence
from stranger_danger.fences.protocol import Coordinate, Fence


@pytest.fixture
def circ() -> Fence:
    return CircularFence(
        name="Test Fence", center=Coordinate(x=2, y=3), radius=1
    )


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
    assert circ.inside_fence(Coordinate(x=3, y=3))


def test_outside_func(circ):
    """Test if a point outside the circle is recognised"""
    assert not circ.inside_fence(Coordinate(x=4, y=5))
