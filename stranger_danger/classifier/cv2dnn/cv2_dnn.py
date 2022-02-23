import pathlib
from typing import Iterable, Tuple

import cv2
import numpy as np

from stranger_danger.classifier.protocol import Image, Prediction, Predictions
from stranger_danger.constants.image_constants import H, W
from stranger_danger.fences.protocol import Coordinate

Predict_Yield = Tuple[str, float, Coordinate, Coordinate]
Oberservation = Iterable[Predict_Yield]

BASE_PATH = pathlib.Path(__file__).parent.absolute()
LABELS = (
    "background",
    "aeroplane",
    "bicycle",
    "bird",
    "boat",
    "bottle",
    "bus",
    "car",
    "cat",
    "chair",
    "cow",
    "diningtable",
    "dog",
    "horse",
    "motorbike",
    "person",
    "pottedplant",
    "sheep",
    "sofa",
    "train",
    "tvmonitor",
)
CONF = 0.3


def yield_prediction(detections: np.ndarray) -> Oberservation:
    detections = detections[0, 0]
    for i in np.arange(0, detections.shape[0]):
        confidence = detections[i, 2]
        if confidence < CONF:
            continue
        label = LABELS[int(detections[i, 1])]
        box = detections[i, 3:7] * np.array([W, H, W, H])
        (startX, startY, endX, endY) = box.astype("int")
        start = Coordinate(x=startX, y=startY)
        end = Coordinate(x=endX, y=endY)
        yield label, confidence, start, end


class Cv2Dnn:
    def __init__(self, name: str = "Cv2 Dnn") -> None:
        self.name = name
        self.labels = LABELS
        self.model = self._setup_model()

    def _setup_model(self) -> cv2.dnn_Net:
        """Initialize the cv2dnn model"""
        return cv2.dnn.readNetFromCaffe(
            f"{BASE_PATH}/requirements/MobileNetSSD_deploy.prototxt.txt",
            f"{BASE_PATH}/requirements/MobileNetSSD_deploy.caffemodel",
        )

    def transform(self, image: np.ndarray) -> Predictions:
        """Predict image and retrun results"""
        image = self._preprocess_image(image)
        return self._predict(image)

    def _preprocess_image(self, image: np.ndarray) -> Image:
        """Preproccess image according too classifier"""
        blob = cv2.dnn.blobFromImage(
            cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5
        )
        return blob

    def _predict(self, image: Image) -> Predictions:
        """Predict using pretrained model"""
        self.model.setInput(image)
        detections = self.model.forward()
        return self._convert_labels(detections)

    def _convert_labels(self, detections: np.ndarray) -> Predictions:
        """Returns the predictions in a uniform way"""
        predictions = []
        for prediction in yield_prediction(detections):
            label, conf, start, end = prediction
            base_point = self._get_base_point(start, end)
            predictions.append(
                Prediction(
                    label=label,
                    point=base_point,
                    bounding_box=(start, end),
                    propability=conf,
                )
            )
        return predictions

    def _get_base_point(self, start: Coordinate, end: Coordinate) -> Coordinate:
        """Returns the base point for every prediction"""
        x_base = int((start.x + end.x) / 2)
        y_base = max((start.y, end.y))
        return Coordinate(x=x_base, y=y_base)
