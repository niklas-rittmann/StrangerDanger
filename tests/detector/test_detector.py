import asyncio
from typing import Sequence

import numpy as np
import pytest
from pydantic import ValidationError

from stranger_danger.classifier import Classifier, Cv2Dnn, Prediction
from stranger_danger.constants.image_constants import H, W
from stranger_danger.detector.detector import Detector
from stranger_danger.email.send_mail import Email
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


@pytest.fixture
def email() -> Email:
    return Email(receivers=["test@mail.de"])


@pytest.fixture
def detector(classifier: Classifier, fences: Fence, email: Email) -> Detector:
    return Detector(classifier=classifier, fences=fences, email=email)


@pytest.mark.parametrize("pred", [(1, 1, True), (11, 11, True), (15, 15, False)])
def test_stranger_in_frame(
    classifier: Classifier, fences: Sequence[Fence], email: Email, pred
):
    """Test if strangers are detected correctly"""
    x, y, _in_fence = pred
    coord = Coordinate(x=x, y=y)
    prediction = (
        Prediction(
            label="person",
            point=coord,
            bounding_box=(coord, coord),
            propability=0.7,
        ),
    )

    det = Detector(classifier=classifier, fences=fences, email=email)
    assert asyncio.run(det.stranger_in_frame(prediction)) == _in_fence


def test_draw_fences(detector: Detector):
    """Draw fences into image"""
    image = np.zeros((H, W, 3), dtype=np.uint8)
    image = asyncio.run(detector.draw_fence_into_image(image))
    assert tuple(image[13, 10, :]) != (0, 0, 0)
    assert tuple(image[4, 4, :]) != (0, 0, 0)


def test_input_validation(
    classifier: Classifier, fences: Sequence[Fence], email: Email
):
    """Test if the input validation raises validation"""
    with pytest.raises(ValidationError):
        Detector(classifier=classifier, fences=fences, email=4)

    with pytest.raises(ValidationError):
        Detector(classifier=classifier, fences=5, email=email)

    with pytest.raises(ValidationError):
        Detector(classifier=3, fences=fences, email=email)
