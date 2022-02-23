from typing import Tuple

import cv2
import numpy as np
from pydantic import BaseModel

from stranger_danger.classifier.protocol import Image
from stranger_danger.constants.image_constants import COLOR, THICKNESS, H, W
from stranger_danger.fences.protocol import Coordinate

Image = np.ndarray
Rec_Coordinates = Tuple[Coordinate, Coordinate]


def _between_points(lower: int, upper: int, coord: int) -> bool:
    """Check if point is located between lower and upper border"""
    lower, upper = sorted([lower, upper])
    return lower < coord < upper


class RectangularFence(BaseModel):

    name: str = "Rectangular Fence"
    coordinates: Rec_Coordinates

    async def draw_fence(self) -> Image:
        """Draw the fence into as blanck image"""
        image = np.zeros((H, W, 3), dtype=np.uint8)
        start_point, end_point = self.coordinates
        return cv2.rectangle(
            image, start_point.tuple, end_point.tuple, COLOR, THICKNESS
        )

    async def inside_fence(self, point: Coordinate) -> bool:
        """Calc if point is in rectangle"""
        first, second = self.coordinates

        return all(
            [
                _between_points(first.x, second.x, point.x),
                _between_points(first.y, second.y, point.y),
            ]
        )
