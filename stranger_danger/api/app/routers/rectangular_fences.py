from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.sql.expression import select

from stranger_danger.db.session import create_session
from stranger_danger.db.tables import Fences
from stranger_danger.fences.rectangular_fence import RectangularFence

router = APIRouter(
    prefix="/rec-fences",
    tags=["rec-fences"],
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
    return RectangularFence.parse_obj(fence.definition)


@router.post("/")
async def create_circular_fence(
    rectangular_fence: RectangularFence, db=Depends(create_session)
):
    """Create and store fence"""
    fence = rectangular_fence
    db.add(Fences(definition=fence.dict()))
    return {"Status": "Added fence to database"}
