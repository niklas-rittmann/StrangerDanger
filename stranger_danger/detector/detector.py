import asyncio
from typing import Sequence, Tuple

import cv2
import numpy as np
from pydantic import BaseModel

from stranger_danger.classifier import Classifier, Predictions
from stranger_danger.classifier.protocol import Prediction
from stranger_danger.constants.image_types import AnnotadedImage, FenceImage
from stranger_danger.db.session import create_context_session
from stranger_danger.db.tables.predictions import Predictions as PredDB
from stranger_danger.email_service.send_mail import EmailConstrutor
from stranger_danger.fences import Fence

Image = np.ndarray
Observation = Sequence[Tuple[Fence, Prediction]]


def _compare_arrays(fence_images: Sequence[FenceImage]) -> FenceImage:
    """Stack fence images vertically, find the max and reshape"""
    shape = fence_images[0].shape
    stacked = np.vstack([image.reshape(1, -1) for image in fence_images])
    max_per_column = stacked.max(axis=0)
    return FenceImage(max_per_column.reshape(shape))


class Detector(BaseModel):
    classifier: Classifier
    fences: Sequence[Fence]
    email: EmailConstrutor

    class Config:
        # Allow own classes like Classifier
        arbitrary_types_allowed = True

    def run_detector(self, image: np.ndarray):
        """Predict using classifier, check fences and finally send email"""
        predictions = self.classifier.transform(image)
        stranger_detected = asyncio.run(self.stranger_in_frame(predictions))
        if stranger_detected:
            # TODO extract max prediction
            _, prediction = stranger_detected[0]
            asyncio.run(self.process_detection(image, prediction))

    async def stranger_in_frame(self, predictions: Predictions) -> Observation:
        """Check if there is a stranger in any of the fences"""
        fence_preds = [
            (fence, pred)
            for fence in self.fences
            for pred in predictions
            if pred.label == "person"
        ]

        tasks = [fence.inside_fence(pred.point) for fence, pred in fence_preds]
        return np.array(fence_preds)[await asyncio.gather(*tasks)].tolist()

    async def process_detection(self, image: Image, prediction: Prediction):
        """Upload to database and send email"""
        image = await self.draw_fence_into_image(image)
        tasks = [
            self.upload_to_database(image, prediction),
            self.send_email(image),
        ]
        await asyncio.gather(*tasks)

    async def draw_fence_into_image(self, image: Image) -> AnnotadedImage:
        """Draw all fences into the image"""
        fences = await asyncio.gather(*[fence.draw_fence() for fence in self.fences])
        fence = _compare_arrays(fences)
        image = cv2.add(image, fence)
        return AnnotadedImage(image)

    @staticmethod
    async def upload_to_database(image: AnnotadedImage, prediction: Prediction):
        """Upload image and corresponding Predicitions to DB"""
        async with create_context_session() as session:
            session.add(
                PredDB(
                    image=cv2.imencode(".jpg", image)[1].tostring(),
                    confidence=prediction.propability,
                )
            )

    async def send_email(self, image: AnnotadedImage):
        await self.email.send_email(image)
