import asyncio
from typing import Sequence

from pydantic import BaseModel

from stranger_danger.classifier import Classifier, Cv2Dnn, Prediction, Predictions
from stranger_danger.fences import CircularFence, Coordinate, Fence, RectangularFence


class Detector(BaseModel):
    classifier: Classifier
    fences: Sequence[Fence]

    class Config:
        # Allow own classes like Classifier
        arbitrary_types_allowed = True

    async def stranger_in_frame(self, predictions: Predictions) -> bool:
        """Check if there is a stranger in any of the fences"""
        tasks = [
            fence.inside_fence(prediction.point)
            for fence in self.fences
            for prediction in predictions
            if prediction.label == "person"
        ]
        return any(await asyncio.gather(*tasks))


# TODO: Added for testing purposes, delete later
if __name__ == "__main__":
    fence_1 = CircularFence(name="Circular", center=Coordinate(x=3, y=3), radius=3)
    fence_2 = RectangularFence(
        name="Rectangular", coordinates=(Coordinate(x=0, y=0), Coordinate(x=4, y=4))
    )
    prediction = (
        Prediction(label="person", point=Coordinate(x=7, y=7), propability=0.7),
    )
    classifier = Cv2Dnn(name="Classifier")

    det = Detector(classifier=classifier, fences=(fence_1, fence_2))
    print(asyncio.run(det.stranger_in_frame(prediction)))
