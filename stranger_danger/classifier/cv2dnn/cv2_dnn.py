import pathlib
from typing import Sequence

import cv2
import numpy as np

from stranger_danger.classifier.protocol import Image, Prediction, Predictions
from stranger_danger.constants.image_constants import H, W
from stranger_danger.fences.protocol import Coordinate

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
CONF = 0.1


class Cv2Dnn:
    def __init__(self, name: str, labels: Sequence[str]) -> None:
        self.name = name
        self.labels = labels

    def _setup_model(self) -> cv2.dnn_Net:
        """Initialize the cv2dnn model"""
        self.model = cv2.dnn.readNetFromCaffe(
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

    def _predict(self, image: Image):
        """Predict using pretrained model"""
        self.model.setInput(image)
        detections = self.model.forward()
        return self._convert_labels(detections)

    def _convert_labels(self, detections: np.ndarray) -> Predictions:
        """Returns the predictions in a uniform way"""
        predictions = []
        for i in np.arange(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > CONF:
                label = LABELS[int(detections[0, 0, i, 1])]
                box = detections[0, 0, i, 3:7] * np.array([W, H, W, H])
                (startX, startY, endX, endY) = box.astype("int")
                base_point = self._get_base_point(
                    Coordinate(x=startX, y=startY), Coordinate(x=endX, y=endY)
                )
                predictions.append(
                    Prediction(label=label, point=base_point, propability=confidence)
                )
        return predictions

    def _get_base_point(self, start: Coordinate, end: Coordinate) -> Coordinate:
        """Returns the base point for every prediction"""
        x_base = int((start.x + end.x) / 2)
        y_base = max((start.y, end.y))
        return Coordinate(x=x_base, y=y_base)


img = cv2.imread("/Users/niklasrittmann/Desktop/IMG_3464.JPG")
model = Cv2Dnn(name="Cv2 Classifier", labels=LABELS)
model._setup_model()
print(model.transform(img))
