from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.sql.expression import select

from stranger_danger.api.app.internal.examples import pent_example
from stranger_danger.db.session import create_session
from stranger_danger.db.tables import Fences
from stranger_danger.fences.pentagon_fence import PentagonFence

router = APIRouter(
    prefix="/pent-fences",
    tags=["pent-fences"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def read_fences(db=Depends(create_session)):
    """Return all the fences"""
    result = (await db.execute(select(Fences))).all()
    if len(result) > 0:
        return result
    raise HTTPException(status_code=404, detail="No Rectangular Fences found!")


@router.get("/{fence_id}")
async def read_fence(fence_id: int, db=Depends(create_session)):
    """Get fences by their id"""
    fence = await db.get(Fences, fence_id)
    return PentagonFence.parse_obj(fence.definition)


@router.post("/")
async def create_circular_fence(
    pentagon_fence: PentagonFence = pent_example,
    db=Depends(create_session),
):
    """Create and store fence"""
    fence = pentagon_fence
    db.add(Fences(definition=fence.dict()))
    return {"Status": "Added fence to database"}
