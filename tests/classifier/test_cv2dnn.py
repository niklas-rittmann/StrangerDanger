import cv2
import numpy as np
import pytest

from stranger_danger.classifier.cv2dnn import cv2_dnn
from stranger_danger.classifier.cv2dnn.cv2_dnn import LABELS, Cv2Dnn, yield_prediction
from stranger_danger.fences.protocol import Coordinate


@pytest.fixture
def dnn_model():
    return Cv2Dnn(name="Test Dnn")


def test_yield_predictions():
    """Test if yield predictions yields the right information"""
    # Example detection [index, label, confidence, x1, y1, x2, y2]
    detections = np.array(
        [
            [
                [
                    [0, 1, 0.5, 0, 0, 3, 3],
                    [0, 2, 0.7, 1, 1, 4, 4],
                ]
            ]
        ]
    )
    label, confidence, start, end = list(yield_prediction(detections))[0]
    assert isinstance(label, str)
    assert isinstance(confidence, float)
    assert isinstance(start, Coordinate)
    assert isinstance(end, Coordinate)


def test_empty_predictions():
    """Test yield function without preictions"""
    detections = np.array([[[[0, 0, 0, 0, 0, 0, 0]]]])
    assert len(list(yield_prediction(detections))) == 0


def test_model_init(dnn_model):
    """Test if the model init works"""
    assert dnn_model.labels == LABELS
    assert dnn_model.name == "Test Dnn"
    assert isinstance(dnn_model.model, cv2.dnn_Net)


def test_preprocess_image(dnn_model):
    """Test the image preprocessing"""
    image = (np.random.rand(400, 600, 3) * 255).astype(np.uint8)
    processed = dnn_model._preprocess_image(image)
    assert processed.shape == (1, 3, 300, 300)
    assert isinstance(processed, np.ndarray)


def test_convert_labels(dnn_model, monkeypatch):
    """Test if the labels are processed and retruned in the right way"""

    def pred(*args):
        yield "tree", 0.7, Coordinate(x=0, y=0), Coordinate(x=2, y=2)

    detections = np.array([[[[0, 0, 0, 0, 0, 0, 0]]]])
    monkeypatch.setattr(cv2_dnn, "yield_prediction", pred)
    predictions = dnn_model._convert_labels(detections)
    assert predictions[0].label == "tree"
    assert predictions[0].propability == 0.7
    assert predictions[0].point == Coordinate(x=1, y=2)


def test_base_point(dnn_model):
    """Test if the base point gets calulated in the right way"""
    start = Coordinate(x=0, y=0)
    end = Coordinate(x=4, y=7)
    point = dnn_model._get_base_point(start, end)
    assert point == Coordinate(x=2, y=7)
