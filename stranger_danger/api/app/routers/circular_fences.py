from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.sql.expression import select

from stranger_danger.db.session import create_session
from stranger_danger.db.tables import Fences
from stranger_danger.fences.circular_fence import CircularFence

router = APIRouter(
    prefix="/circ-fences",
    tags=["circ-fences"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def read_fences(db=Depends(create_session)):
    """Return all the fences"""
    result = (await db.execute(select(Fences))).all()
    if len(result) > 0:
        return result
    raise HTTPException(status_code=404, detail="No CircularFences found!")


@router.get("/{fence_id}")
async def read_fence(fence_id: int, db=Depends(create_session)):
    """Get fences by their id"""
    fence = await db.get(Fences, fence_id)
    return CircularFence.parse_obj(fence.definition)


@router.post("/")
async def create_circular_fence(
    circular_fence: CircularFence, db=Depends(create_session)
):
    """Create and store fence"""
    fence = circular_fence
    db.add(Fences(definition=fence.dict()))
    return {"Status": "Added fence to database"}
