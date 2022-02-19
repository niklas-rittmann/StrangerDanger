from typing import Protocol

from pydantic.main import BaseModel


class Coordinate(BaseModel):
    x: int
    y: int


class Fence(Protocol):

    name: str

    def inside_fence(self, point: Coordinate) -> bool:
        """Check if given coordinate in Fence"""
        ...
