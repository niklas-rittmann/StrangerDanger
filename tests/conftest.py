from typing import Sequence

import pytest

from stranger_danger.classifier import Classifier, Cv2Dnn
from stranger_danger.detector.detector import Detector
from stranger_danger.email_service.send_mail import EmailConstrutor
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
def email() -> EmailConstrutor:
    return EmailConstrutor(receivers=["test@mail.de"])


@pytest.fixture
def detector(classifier: Classifier, fences: Fence, email: EmailConstrutor) -> Detector:
    return Detector(classifier=classifier, fences=fences, email=email)
