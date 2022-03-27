from pathlib import Path

from fastapi import HTTPException
from pydantic.networks import EmailStr
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql.expression import select

from stranger_danger.api.app.routers.fences import fence_from_db
from stranger_danger.classifier.cv2dnn.cv2_dnn import Cv2Dnn
from stranger_danger.db.tables.areas import Areas
from stranger_danger.db.tables.email import Email
from stranger_danger.db.tables.fences import Fences
from stranger_danger.detector.detector import Detector
from stranger_danger.detector.event_listener import FilesytemWatcher
from stranger_danger.email_service.send_mail import EmailConstrutor
from stranger_danger.fences.protocol import Fence


async def run(db: AsyncSession, area_id: int) -> FilesytemWatcher:
    """Run a detecor"""
    path_to_watch = await get_directory(db, area_id)
    detector = await compose_detector(db, area_id)
    watcher = FilesytemWatcher(detector, path_to_watch)
    watcher.run_watcher()
    return watcher


async def get_directory(db: AsyncSession, area_id: int) -> Path:
    """Fetch the directories to watch from the databse"""
    result = await db.execute(select(Areas).where(Areas.id == area_id))
    if result:
        return Path(result.scalars().first().directory)
    raise HTTPException(status_code=404, detail=f"No area with area id:{area_id}")


async def compose_detector(db: AsyncSession, area_id: int) -> Detector:
    """Compose a detector to monitor strangers"""
    classifier = Cv2Dnn()
    emails = await fetch_emails_from_db(db, area_id)
    email = EmailConstrutor(receivers=emails)
    fences = await fetch_fences_from_db(db, area_id)
    detector = Detector(classifier=classifier, fences=fences, email=email)
    return detector


async def fetch_emails_from_db(db: AsyncSession, area_id: int) -> list[EmailStr]:
    """Fetch the emails from database"""
    result = await db.execute(select(Email).where(Email.area == area_id))
    emails = [email.address for email in result.scalars()]
    if not emails:
        raise HTTPException(status_code=404, detail="No email found!")
    return emails


async def fetch_fences_from_db(db: AsyncSession, area_id: int) -> list[Fence]:
    """Fetch the fences from database"""
    result = await db.execute(select(Fences).where(Fences.area == area_id))
    fences = [fence_from_db(fence) for fence in result.scalars()]
    if not fences:
        raise HTTPException(status_code=404, detail="No fences found!")
    return fences
