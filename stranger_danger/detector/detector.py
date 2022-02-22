import asyncio
from os import wait
from typing import Sequence

import numpy as np
from pydantic import BaseModel

from stranger_danger.classifier import Classifier, Cv2Dnn, Prediction, Predictions
from stranger_danger.email.send_mail import Email
from stranger_danger.fences import CircularFence, Coordinate, Fence, RectangularFence


class Detector(BaseModel):
    classifier: Classifier
    fences: Sequence[Fence]
    email: Email

    class Config:
        # Allow own classes like Classifier
        arbitrary_types_allowed = True

    async def run_detector(self, image: np.ndarray):
        """Predict using classifier, check fences and finally send email"""
        predictions = self.classifier.transform(image)
        stranger_detected = asyncio.run(self.stranger_in_frame(predictions))
        tasks = [self.upload_to_database(image, predictions)]
        if stranger_detected:
            tasks.append(self.send_email(image))
        asyncio.run(*tasks)

    async def stranger_in_frame(self, predictions: Predictions) -> bool:
        """Check if there is a stranger in any of the fences"""
        tasks = [
            fence.inside_fence(prediction.point)
            for fence in self.fences
            for prediction in predictions
            if prediction.label == "person"
        ]
        return any(await asyncio.gather(*tasks))

    @staticmethod
    async def upload_to_database(image: np.ndarray, predictions: Predictions):
        """Upload image and corresponding Predicitions to DB"""
        print("Uploaded to Databse")

    @staticmethod
    async def send_email(image: np.ndarray):
        print("Send Email")
