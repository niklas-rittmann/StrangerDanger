import math
from stranger_danger.fences.protocol import Coordinate
from pydantic import BaseModel

Radius = int


def square_root_distance(base: Coordinate, target: Coordinate) -> float:
    return math.sqrt((base.x - target.x) ** 2 + (base.y - target.y) ** 2)


class CircularFence(BaseModel):

    name: str = "Circular Fence"
    center: Coordinate
    radius: Radius

    def inside_fence(self, point: Coordinate) -> bool:
        """Calc if point is in circle"""
        return square_root_distance(self.center, point) <= self.radius
