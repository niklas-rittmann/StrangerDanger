from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql.expression import select

from stranger_danger.api.app.internal.auth.auth import auth_handler
from stranger_danger.api.app.internal.auth.schema import AuthDetails
from stranger_danger.db.session import create_session
from stranger_danger.db.tables.users import Users

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


async def get_user_from_db(db: AsyncSession, username: str) -> Users:
    """Get user from databse"""
    user = await db.execute(select(Users).where(Users.username == username))
    return user.scalars().first()


@router.post("/register", status_code=201)
async def register(auth_details: AuthDetails, db=Depends(create_session)):
    """Register a new user"""
    user = await get_user_from_db(db, auth_details.username)
    if user:
        raise HTTPException(status_code=400, detail="Username is taken")
    hashed = auth_handler.get_password_hash(auth_details.password)
    db.add(Users(username=auth_details.username, password=hashed))
    return


@router.post("/login")
async def login(auth_details: AuthDetails, db=Depends(create_session)):
    """Login an existing user"""
    user = await get_user_from_db(db, auth_details.username)
    if (user is None) or (
        not auth_handler.verify_password(auth_details.password, user.password)
    ):
        raise HTTPException(status_code=401, detail="Invalid username and or password")
    token = auth_handler.encode_token(user.username)
    return {"token": token}


@router.get("/protected")
def protected(username=Depends(auth_handler.auth_wrapper)):
    return {"name": username}
