import base64

from fastapi import APIRouter, Depends
from sqlalchemy.sql.expression import select

from stranger_danger.api.app.internal.auth.auth import auth_handler
from stranger_danger.api.app.internal.predictions.schema import PredictionBase
from stranger_danger.db.session import create_session
from stranger_danger.db.tables.predictions import Predictions

router = APIRouter(
    prefix="/predictions",
    tags=["predictions"],
    dependencies=[Depends(auth_handler.auth_wrapper)],
    responses={404: {"description": "Not found"}},
)


def image_from_str(image: bytes) -> bytes:
    """Return image from string"""
    return base64.b64encode(image)


@router.get("/")
async def read_predictions(db=Depends(create_session)):
    """Return all the predictions"""
    result = await db.execute(select(Predictions).order_by(Predictions.date))
    return [
        PredictionBase(id=pred.id, image=image_from_str(pred.image), date=pred.date)
        for pred in result.scalars()
    ]


# TODO: Add area id to predictions
