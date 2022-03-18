from fastapi import APIRouter, Depends

from stranger_danger.api.app.internal.cache import watcher_cache
from stranger_danger.api.app.internal.detector import create, schema
from stranger_danger.db.session import create_session

router = APIRouter(
    prefix="/detector",
    tags=["detector"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{area_id}")
async def detector_status(area_id: int):
    """Get the detector status"""
    watcher = watcher_cache.get_item(area_id)
    if watcher:
        return schema.DetectorRunning(area_id=area_id, running=watcher.is_running)
    return schema.DetectorRunning(area_id=area_id, running=False)


@router.post("/start/{area_id}")
async def start_detector(area_id: int, db=Depends(create_session)):
    """Start the detector"""
    if watcher_cache.get_item(area_id):
        return schema.DetectorRunning(area_id=area_id, running=True)
    watcher_cache.add(area_id, await create.run(db, area_id))
    return schema.DetectorChanged(area_id=area_id, status="started")


@router.post("/stop/{area_id}")
async def stop_detector(area_id: int):
    """Stop the detector"""
    watcher = watcher_cache.get_item(area_id)
    if not watcher:
        return schema.DetectorRunning(area_id=area_id, running=False)
    watcher.stop_watcher()
    watcher_cache.remove(area_id)
    return schema.DetectorChanged(area_id=area_id, status="stopped")
