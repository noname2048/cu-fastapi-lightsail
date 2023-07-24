from fastapi import APIRouter

from .sensor import router as sensor_router
from .sensor_record import router as sensor_record_router

router = APIRouter()
router.include_router(sensor_router, prefix="/sensors", tags=["sensors"])
router.include_router(
    sensor_record_router, prefix="/sensor_records", tags=["sensors_records"]
)


@router.get("/v1/hello")
async def hello():
    return {"message": "hello"}
