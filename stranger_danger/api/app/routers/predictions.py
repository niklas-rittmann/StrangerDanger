from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.sql.expression import delete, select

from stranger_danger.api.app.internal.areas.path import check_store_area
from stranger_danger.api.app.internal.areas.schema import AreaBase
from stranger_danger.api.app.internal.auth.auth import auth_handler
from stranger_danger.api.app.internal.cache import watcher_cache
from stranger_danger.db.session import create_session
from stranger_danger.db.tables.areas import Areas
from stranger_danger.detector.event_listener import DIRECTORY_TO_WATCH

router = APIRouter(
    prefix="/areas",
    tags=["areas"],
    dependencies=[Depends(auth_handler.auth_wrapper)],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def read_areas(db=Depends(create_session)):
    """Return all the areas"""
    result = await db.execute(select(Areas))
    return {area.id: area.directory for area in result.scalars()}


@router.post("/")
async def create_area(path: str, db=Depends(create_session)):
    """Create and store area"""
    watch_dir = f"{DIRECTORY_TO_WATCH}/{path}"
    return await check_store_area(db, watch_dir)


@router.delete("/{area_id}")
async def delete_area(area_id: int, db=Depends(create_session)):
    """Delte area by id"""
    if watcher_cache.get_item(area_id):
        raise HTTPException(
            status_code=404, detail="Watcher still running, stop before removing area"
        )
    await db.execute(delete(Areas).where(Areas.id == area_id))
    return AreaBase(id=area_id, status="Removed area")
