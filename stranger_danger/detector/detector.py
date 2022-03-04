import asyncio
from typing import NewType, Sequence

import cv2
import numpy as np
from pydantic import BaseModel

from stranger_danger.classifier import Classifier, Predictions
from stranger_danger.email.send_mail import EmailConstrutor
from stranger_danger.fences import Fence

Image = np.ndarray
AnnotadedImage = NewType("AnnotadedImage", np.ndarray)


class Detector(BaseModel):
    classifier: Classifier
    fences: Sequence[Fence]
    email: EmailConstrutor

    class Config:
        # Allow own classes like Classifier
        arbitrary_types_allowed = True

    async def run_detector(self, image: np.ndarray):
        """Predict using classifier, check fences and finally send email"""
        predictions = self.classifier.transform(image)
        stranger_detected = asyncio.run(self.stranger_in_frame(predictions))
        if stranger_detected:
            image = asyncio.run(self.draw_fence_into_image(image))
            tasks = [
                self.upload_to_database(image, predictions),
                self.send_email(image),
            ]
            asyncio.run(*tasks)

    async def draw_fence_into_image(self, image: Image) -> AnnotadedImage:
        """Draw all fences into the image"""
        fences = await asyncio.gather(*[fence.draw_fence() for fence in self.fences])
        fence = np.maximum(*fences)
        image = cv2.add(image, fence)
        return AnnotadedImage(image)

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
    async def upload_to_database(image: AnnotadedImage, predictions: Predictions):
        """Upload image and corresponding Predicitions to DB"""
        print("Uploaded to Databse")

    @staticmethod
    async def send_email(image: AnnotadedImage):
        print("Send Email")
