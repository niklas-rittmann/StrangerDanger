from dataclasses import dataclass

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql.expression import select
from sqlalchemy.sql.sqltypes import JSON

from stranger_danger.api.app.internal.examples import pent_example, rec_example
from stranger_danger.db.session import create_session
from stranger_danger.db.tables import Fences
from stranger_danger.fences.circular_fence import CircularFence
from stranger_danger.fences.pentagon_fence import PentagonFence
from stranger_danger.fences.protocol import Fence
from stranger_danger.fences.rectangular_fence import RectangularFence


@dataclass(frozen=True)
class FenceMapper:
    Circular = CircularFence
    Pentagon = PentagonFence
    Rectangular = RectangularFence


def _upload_fence(db: AsyncSession, payload: Fence, fence_type: str):
    """Helper to upload the fences"""
    db.add(Fences(definition=payload.dict(), type=fence_type))


router = APIRouter(
    prefix="/pent-fences",
    tags=["pent-fences"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def read_fences(db=Depends(create_session)):
    """Return all the fences"""
    result = await db.execute(select(Fences))
    return [
        getattr(FenceMapper, fence.type).parse_obj(fence.definition)
        for fence in result.scalars()
    ]


@router.get("/{fence_id}")
async def read_fence(fence_id: int, db=Depends(create_session)):
    """Get fences by their id"""
    fence = await db.get(Fences, fence_id)
    if fence is None:
        raise HTTPException(status_code=404, detail=f"No fence with id {fence_id}")
    return getattr(FenceMapper, fence.type).parse_obj(fence.definition)


@router.post("/circular")
async def create_circular_fence(
    circular_fence: CircularFence,
    db=Depends(create_session),
):
    """Create and store fence"""
    _upload_fence(db, circular_fence, "Circular")
    return {"Status": "Added fence to database"}


@router.post("/rectangular")
async def create_rectangular_fence(
    rectangular_fence: RectangularFence = rec_example,
    db=Depends(create_session),
):
    """Create and store fence"""
    _upload_fence(db, rectangular_fence, "Rectangular")
    return {"Status": "Added fence to database"}


@router.post("/pentagon")
async def create_pentragon_fence(
    pentagon_fence: PentagonFence = pent_example,
    db=Depends(create_session),
):
    """Create and store fence"""
    _upload_fence(db, pentagon_fence, "Pentagon")
    return {"Status": "Added fence to database"}
