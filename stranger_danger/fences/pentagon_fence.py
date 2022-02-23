from typing import Tuple

import cv2
import numpy as np
from matplotlib import path
from pydantic import BaseModel

from stranger_danger.classifier.protocol import Image
from stranger_danger.constants.image_constants import COLOR, THICKNESS, H, W
from stranger_danger.fences.protocol import Coordinate

Image = np.ndarray
Pent_Coordinates = Tuple[Coordinate, Coordinate, Coordinate, Coordinate, Coordinate]


def _inside_pentagon(coordinates: Pent_Coordinates, point: Coordinate) -> bool:
    """Calculate if a point is inside a pentagon"""
    pentagon = path.Path([[coord.x, coord.y] for coord in coordinates])
    return pentagon.contains_point((point.x, point.y), radius=0.1)


class PentagonFence(BaseModel):

    name: str = "Pentagon Fence"
    coordinates: Pent_Coordinates

    async def draw_fence(self) -> Image:
        """Draw the fence into as blanck image"""
        image = np.zeros((H, W, 3), dtype=np.uint8)
        coord = np.array([coord.tuple for coord in self.coordinates])
        return cv2.polylines(image, [coord], True, COLOR, THICKNESS)

    async def inside_fence(self, point: Coordinate) -> bool:
        """Calc if point is in pentagon"""
        return _inside_pentagon(self.coordinates, point)
