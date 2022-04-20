from datetime import datetime

from pydantic import BaseModel


class PredictionBase(BaseModel):
    id: int
    image: bytes
    date: datetime
