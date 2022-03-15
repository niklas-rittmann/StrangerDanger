from typing import Tuple

import cv2
import numpy as np
from matplotlib import path
from pydantic import BaseModel, Field

from stranger_danger.constants.image_constants import COLOR, THICKNESS, H, W
from stranger_danger.constants.image_types import FenceImage
from stranger_danger.fences.protocol import Coordinate

PentCoordinates = Tuple[Coordinate, Coordinate, Coordinate, Coordinate, Coordinate]


class PentagonFence(BaseModel):

    name: str = "Pentagon Fence"
    coordinates: PentCoordinates
    type: str = Field("Pentagon", const=True)

    async def draw_fence(self) -> FenceImage:
        """Draw the fence into as blanck image"""
        image = np.zeros((H, W, 3), dtype=np.uint8)
        coord = np.array([coord.as_tuple for coord in self.coordinates])
        return cv2.polylines(image, [coord], True, COLOR, THICKNESS)

    async def inside_fence(self, point: Coordinate) -> bool:
        """Calc if point is in pentagon"""
        pentagon = path.Path([[coord.x, coord.y] for coord in self.coordinates])
        return pentagon.contains_point((point.x, point.y), radius=0.1)
