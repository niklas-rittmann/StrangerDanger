from dataclasses import dataclass
from typing import Union

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.sql.expression import delete, select

from stranger_danger.api.app.internal.examples import fence_examples
from stranger_danger.db.queries import get_by_id
from stranger_danger.db.session import create_session
from stranger_danger.db.tables import Fences
from stranger_danger.db.tables.areas import Areas
from stranger_danger.fences.circular_fence import CircularFence
from stranger_danger.fences.pentagon_fence import PentagonFence
from stranger_danger.fences.protocol import Fence
from stranger_danger.fences.rectangular_fence import RectangularFence


@dataclass(frozen=True)
class FenceMapper:
    Circular = CircularFence
    Pentagon = PentagonFence
    Rectangular = RectangularFence


router = APIRouter(
    prefix="/fences",
    tags=["fences"],
    responses={404: {"description": "Not found"}},
)


def fence_from_db(fence: Fences) -> Fence:
    return getattr(FenceMapper, str(fence.type)).parse_obj(fence.definition)


@router.get("/")
async def read_fences(db=Depends(create_session)):
    """Return all the fences"""
    result = await db.execute(select(Fences))
    return [
        {"id": fence.id, "value": fence_from_db(fence)} for fence in result.scalars()
    ]


@router.get("/{fence_id}")
async def read_fence_by_id(fence_id: int, db=Depends(create_session)):
    """Get fences by their id"""
    fence = await get_by_id(db, Fences, fence_id)
    if fence is None:
        raise HTTPException(status_code=404, detail=f"No fence with id {fence_id}")
    return getattr(FenceMapper, fence.type).parse_obj(fence.definition)


@router.post("/{area_id}")
async def create_fence(
    area_id: int,
    fence: Union[CircularFence, RectangularFence, PentagonFence] = fence_examples,
    db=Depends(create_session),
):
    """Create and store fence"""
    if not await get_by_id(db, Areas, area_id):
        raise HTTPException(
            status_code=404, detail=f"No Area defined with id {area_id}"
        )
    db.add(Fences(area=area_id, definition=fence.dict(), type=fence.type))
    return {"Status": "Added fence to database"}


@router.delete("/{fence_id}")
async def delete_fence(fence_id: int, db=Depends(create_session)):
    """Delte fence by id"""
    await db.execute(delete(Fences).where(Fences.id == fence_id))
    return {"Status": f"Deleted fence with id {fence_id}"}
