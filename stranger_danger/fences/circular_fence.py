import math

import cv2
import numpy as np
from pydantic import BaseModel

from stranger_danger.constants.image_constants import COLOR, THICKNESS, H, W
from stranger_danger.fences.protocol import Coordinate, FenceImage

Radius = int


def _square_root_distance(base: Coordinate, target: Coordinate) -> float:
    """Calculate the root square distance of two points"""
    return math.sqrt((base.x - target.x) ** 2 + (base.y - target.y) ** 2)


class CircularFence(BaseModel):

    name: str = "Circular Fence"
    center: Coordinate
    radius: Radius

    async def draw_fence(self) -> FenceImage:
        """Draw the fence into as blanck image"""
        image = np.zeros((H, W, 3), dtype=np.uint8)
        return cv2.circle(image, self.center.as_tuple, self.radius, COLOR, THICKNESS)

    async def inside_fence(self, point: Coordinate) -> bool:
        """Calc if point is in circle"""
        return _square_root_distance(self.center, point) <= self.radius
