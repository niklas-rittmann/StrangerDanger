from typing import NewType, Protocol, Tuple

import numpy as np
from pydantic.main import BaseModel

FenceImage = NewType("FenceImage", np.ndarray)


class Coordinate(BaseModel):
    x: int
    y: int

    @property
    def as_tuple(self) -> Tuple[int, int]:
        """Return tuple representation of coordinate"""
        return (self.x, self.y)


class Fence(Protocol):

    name: str

    async def draw_fence(self) -> FenceImage:
        """Draw the fence into an empty image"""
        ...

    async def inside_fence(self, point: Coordinate) -> bool:
        """Check if given coordinate in Fence"""
        ...
