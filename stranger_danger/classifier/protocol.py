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

    def _preprocess_image(self, image: np.ndarray) -> Image:
        """Preproccess image according too classifier"""
        ...

    def _predict(self, image: Image):
        """Predict using pretrained model"""
        ...

    def _convert_labels(self) -> Predictions:
        """Returns the predictions in a uniform way"""
        ...

    def _get_base_point(self) -> Coordinate:
        """Returns the base point for every prediction"""
        ...
