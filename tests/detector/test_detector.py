import asyncio
from typing import Sequence

import pytest
from pydantic import ValidationError

from stranger_danger.classifier import Classifier, Cv2Dnn, Prediction
from stranger_danger.detector.detector import Detector
from stranger_danger.fences import CircularFence, Coordinate, Fence, RectangularFence


@pytest.fixture
def classifier() -> Classifier:
    return Cv2Dnn(name="Classifier")


@pytest.fixture
def fences() -> Sequence[Fence]:
    fence_1 = CircularFence(name="Circular", center=Coordinate(x=10, y=10), radius=3)
    fence_2 = RectangularFence(
        name="Rectangular", coordinates=(Coordinate(x=0, y=0), Coordinate(x=4, y=4))
    )
    return (fence_1, fence_2)


@pytest.mark.parametrize("pred", [(1, 1, True), (11, 11, True), (15, 15, False)])
def test_stranger_in_frame(classifier: Classifier, fences: Sequence[Fence], pred):
    """Test if strangers are detected correctly"""
    x, y, _in_fence = pred
    coord = Coordinate(x=x, y=y)
    prediction = (
        Prediction(
            label="person",
            point=Coordinate(x=x, y=y),
            bounding_box=(coord, coord),
            propability=0.7,
        ),
    )

    det = Detector(classifier=classifier, fences=fences)
    assert asyncio.run(det.stranger_in_frame(prediction)) == _in_fence


def test_input_validation():
    """Test if the input validation raises validation"""

    with pytest.raises(ValidationError):
        Detector(classifier=3, fences=5)
