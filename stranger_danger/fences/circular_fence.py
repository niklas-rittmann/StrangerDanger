import math

from pydantic import BaseModel

from stranger_danger.fences.protocol import Coordinate

Radius = int


def _square_root_distance(base: Coordinate, target: Coordinate) -> float:
    """Calculate the root square distance of two points"""
    return math.sqrt((base.x - target.x) ** 2 + (base.y - target.y) ** 2)


class CircularFence(BaseModel):

    name: str = "Circular Fence"
    center: Coordinate
    radius: Radius

    def inside_fence(self, point: Coordinate) -> bool:
        """Calc if point is in circle"""
        return _square_root_distance(self.center, point) <= self.radius
