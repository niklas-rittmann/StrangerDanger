from pydantic import BaseModel


class DetectorBase(BaseModel):
    area_id: int


class DetectorRunning(DetectorBase):
    running: bool


class DetectorChanged(DetectorBase):

    status: str
