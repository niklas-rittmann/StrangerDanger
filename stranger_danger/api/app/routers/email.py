from fastapi import APIRouter, Depends, HTTPException
from pydantic.main import BaseModel
from pydantic.networks import EmailStr
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql.expression import and_, select

from stranger_danger.api.app.internal.auth.auth import auth_handler
from stranger_danger.db.queries import get_by_id
from stranger_danger.db.session import create_session
from stranger_danger.db.tables.areas import Areas
from stranger_danger.db.tables.email import Email

router = APIRouter(
    prefix="/emails",
    tags=["emails"],
    dependencies=[Depends(auth_handler.auth_wrapper)],
    responses={404: {"description": "Not found"}},
)


class EmailSchema(BaseModel):
    address: EmailStr
    area: int


class EmailId(EmailSchema):
    id: int


class EmailStatus(EmailSchema):
    status: str


async def get_email_from_db(db: AsyncSession, email: EmailStr, area: int) -> Email:
    """Get user from database"""
    emails = await db.execute(
        select(Email).where(and_(Email.address == email, Email.area == area))
    )
    return emails.scalars().first()


@router.get("/", status_code=200)
async def get_emails(db=Depends(create_session)):
    """Get stored emails"""

    email = await db.execute(select(Email))
    emails = [
        EmailId(address=mail.address, area=mail.area, id=mail.id)
        for mail in email.scalars()
    ]
    if not emails:
        raise HTTPException(status_code=400, detail="No emails found")

    return emails


@router.post("/{area_id}")
async def add_email(area_id: int, email: EmailStr, db=Depends(create_session)):
    """Add email to databse"""
    if not await get_by_id(db, Areas, area_id):
        raise HTTPException(
            status_code=404, detail=f"No Area defined with id {area_id}"
        )
    if await get_email_from_db(db, email, area_id):
        raise HTTPException(
            status_code=401, detail="Email area_id combination already exists"
        )
    db.add(Email(address=email, area=area_id))
    return EmailStatus(status="added", address=email, area=area_id)


@router.delete("/")
async def remove_email(id: int, db=Depends(create_session)):
    """Remove email from databse"""
    if not await get_by_id(db, Email, id):
        raise HTTPException(status_code=401, detail="Email doesnt exist")
    email = await db.execute(select(Email).where(Email.id == id))
    mail = email.scalars().first()
    await db.delete(mail)
    return EmailStatus(status="removed", address=mail.address, area=mail.area)
