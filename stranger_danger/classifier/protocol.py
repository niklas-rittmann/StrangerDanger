from typing import Any, Optional, Protocol, Sequence

import numpy as np
from pydantic import BaseModel

from stranger_danger.fences.protocol import Coordinate


class Prediction(BaseModel):
    label: str
    point: Coordinate
    propability: float


Predictions = Sequence[Prediction]
Image = np.ndarray


class Classifier(Protocol):

    name: str
    labels: Sequence[str]
    model: Optional[Any]

    def _setup_model(self) -> Any:
        """Setup the classfier model"""
        ...

    def transform(self, image: np.ndarray) -> Predictions:
        """Predict and extract labels"""
        ...

    def _preprocess_image(self, image: np.ndarray) -> Image:
        """Preproccess image according too classifier"""
        ...

    def _predict(self, image: Image) -> Predictions:
        """Predict using pretrained model"""
        ...

    def _convert_labels(self, detections: np.array) -> Predictions:
        """Returns the predictions in a uniform way"""
        ...

    def _get_base_point(self, start: Coordinate, end: Coordinate) -> Coordinate:
        """Returns the base point for every prediction"""
        ...
