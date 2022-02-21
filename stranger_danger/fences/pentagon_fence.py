from typing import Tuple

from matplotlib import path
from pydantic import BaseModel

from stranger_danger.fences.protocol import Coordinate

Pent_Coordinates = Tuple[Coordinate, Coordinate, Coordinate, Coordinate, Coordinate]


def _inside_pentagon(coordinates: Pent_Coordinates, point: Coordinate) -> bool:
    """Calculate if a point is inside a pentagon"""
    pentagon = path.Path([[coord.x, coord.y] for coord in coordinates])
    return pentagon.contains_point((point.x, point.y), radius=0.1)


class PentagonFence(BaseModel):

    name: str = "Pentagon Fence"
    coordinates: Pent_Coordinates

    async def inside_fence(self, point: Coordinate) -> bool:
        """Calc if point is in pentagon"""
        return _inside_pentagon(self.coordinates, point)
