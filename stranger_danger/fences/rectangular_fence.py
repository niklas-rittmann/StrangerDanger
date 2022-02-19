from typing import Tuple

from pydantic import BaseModel

from stranger_danger.fences.protocol import Coordinate

Rec_Coordinates = Tuple[Coordinate, Coordinate]


def _between_points(lower: int, upper: int, coord: int) -> bool:
    """Check if point is located between lower and upper border"""
    lower, upper = sorted([lower, upper])
    return lower < coord < upper


class RectangularFence(BaseModel):

    name: str = "Rectangular Fence"
    coordinates: Rec_Coordinates
    center: None = None
    radius: None = None

    def inside_fence(self, point: Coordinate) -> bool:
        """Calc if point is in circle"""
        first, second = self.coordinates

        return all(
            [
                _between_points(first.x, second.x, point.x),
                _between_points(first.y, second.y, point.y),
            ]
        )
