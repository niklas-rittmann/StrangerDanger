import os

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql.expression import delete, select

from stranger_danger.api.app.internal.cache import watcher_cache
from stranger_danger.api.app.routers.fences import fence_from_db
from stranger_danger.classifier.cv2dnn.cv2_dnn import Cv2Dnn
from stranger_danger.db.session import create_session
from stranger_danger.db.tables import Fences
from stranger_danger.detector.detector import Detector
from stranger_danger.detector.event_listener import FilesytemWatcher
from stranger_danger.email_service.send_mail import EmailConstrutor
from stranger_danger.fences.circular_fence import CircularFence
from stranger_danger.fences.pentagon_fence import PentagonFence
from stranger_danger.fences.protocol import Fence
from stranger_danger.fences.rectangular_fence import RectangularFence
from tests.conftest import classifier, detector

router = APIRouter(
    prefix="/detector",
    tags=["detector"],
    responses={404: {"description": "Not found"}},
)


async def create_detector(db: AsyncSession) -> Detector:
    """Compose a detector to monitor strangers"""
    classifier = Cv2Dnn()
    email = EmailConstrutor(receivers=[os.getenv("EMAIL_RECEIVER")])
    fences = await fetch_fences_from_db(db)
    if not fences:
        raise HTTPException(status_code=404, detail=f"No fences found!")
    detector = Detector(classifier=classifier, fences=fences, email=email)
    return detector


async def fetch_fences_from_db(db: AsyncSession) -> list[Fence]:
    """Fetch the fences from database"""
    result = await db.execute(select(Fences))
    return [fence_from_db(fence) for fence in result.scalars()]


@router.get("/")
async def detector_status():
    """Get the detector status"""
    watcher = watcher_cache.get_item("Watcher")
    if watcher:
        return {"Status": watcher.is_running}
    return {"Status": "No watcher running"}


@router.post("/start")
async def start_detector(db=Depends(create_session)):
    """Start the detector"""
    if watcher_cache.get_item("Watcher"):
        return {"Status": "Watcher already running"}
    detector = await create_detector(db)
    watcher = FilesytemWatcher(detector, True)
    watcher.run_watcher()
    watcher_cache.add("Watcher", watcher)
    return {"Status": "Started Watcher"}


@router.post("/stop")
async def stop_detector():
    """Stop the detector"""
    watcher = watcher_cache.get_item("Watcher")
    if not watcher:
        return {"Status": "No Watcher running"}
    watcher.stop_watcher()
    watcher_cache.remove("Watcher")
    return {"Status": "Stopped watcher"}
