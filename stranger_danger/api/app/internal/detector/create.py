import os

from fastapi import HTTPException
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql.expression import select

from stranger_danger.api.app.routers.fences import fence_from_db
from stranger_danger.classifier.cv2dnn.cv2_dnn import Cv2Dnn
from stranger_danger.db.tables.fences import Fences
from stranger_danger.detector.detector import Detector
from stranger_danger.detector.event_listener import FilesytemWatcher
from stranger_danger.email_service.send_mail import EmailConstrutor
from stranger_danger.fences.protocol import Fence


async def run(db: AsyncSession, area_id: int) -> FilesytemWatcher:
    """Run a detecor"""
    detector = await compose_detector(db, area_id)
    watcher = FilesytemWatcher(detector, True)
    watcher.run_watcher()
    return watcher


async def compose_detector(db: AsyncSession, area_id: int) -> Detector:
    """Compose a detector to monitor strangers"""
    classifier = Cv2Dnn()
    email = EmailConstrutor(receivers=[os.getenv("EMAIL_RECEIVER")])
    fences = await fetch_fences_from_db(db, area_id)
    detector = Detector(classifier=classifier, fences=fences, email=email)
    return detector


async def fetch_fences_from_db(db: AsyncSession, area_id: int) -> list[Fence]:
    """Fetch the fences from database"""
    result = await db.execute(select(Fences).where(Fences.area == area_id))
    fences = [fence_from_db(fence) for fence in result.scalars()]
    if not fences:
        raise HTTPException(status_code=404, detail="No fences found!")
    return fences
