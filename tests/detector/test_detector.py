import asyncio
from typing import Sequence

import numpy as np
import pytest
from pydantic import ValidationError

from stranger_danger.classifier import Classifier, Prediction
from stranger_danger.constants.image_constants import H, W
from stranger_danger.detector.detector import Detector, _compare_arrays
from stranger_danger.email_service.send_mail import EmailConstrutor
from stranger_danger.fences import Coordinate, Fence


@pytest.mark.parametrize("pred", [(1, 1, True), (11, 11, True), (15, 15, False)])
def test_stranger_in_frame(
    classifier: Classifier, fences: Sequence[Fence], email: EmailConstrutor, pred
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
    classifier: Classifier, fences: Sequence[Fence], email: EmailConstrutor
):
    """Test if the input validation raises validation"""
    with pytest.raises(ValidationError):
        Detector(classifier=classifier, fences=fences, email=4)

    with pytest.raises(ValidationError):
        Detector(classifier=classifier, fences=5, email=email)

    with pytest.raises(ValidationError):
        Detector(classifier=3, fences=fences, email=email)


def test_max_from_arrays():
    arr_1 = np.array([[1, 2, 3], [1, 2, 3], [1, 2, 3]])
    arr_2 = np.array([[3, 2, 1], [1, 2, 3], [3, 3, 3]])
    output = _compare_arrays([arr_1, arr_2])
    expected = np.array([[3, 2, 3], [1, 2, 3], [3, 3, 3]])
    np.testing.assert_array_equal(output, expected)
