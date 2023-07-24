from fastapi import APIRouter, Body, Path
from sqlalchemy import select

from ..database import SessionLocal
from ..models import Sensor
from ..schemas import SensorCreateRequest

router = APIRouter()


@router.get("")
async def list_sensor():
    with SessionLocal() as session:
        stmt = select(Sensor)
        sensors = session.execute(stmt).scalars().all()
    return sensors


@router.get("/{uuid}")
async def retrieve_sensor(uuid: str = Path(...)):
    with SessionLocal() as session:
        stmt = select(Sensor).where(Sensor.uuid == uuid)
        sensor = session.execute(stmt).scalar_one_or_none()

    return sensor


@router.post("")
async def create_sensor(body: SensorCreateRequest = Body(...)):
    with SessionLocal() as session:
        db_sensor = Sensor(name=body.name)
        session.add(db_sensor)
        session.commit()
        session.refresh(db_sensor)

    return db_sensor
