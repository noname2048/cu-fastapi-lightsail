from datetime import datetime, timedelta

from fastapi import APIRouter, Body, Path, Query, status
from fastapi.exceptions import HTTPException
from pydantic import UUID4
from sqlalchemy import select

from ..database import SessionLocal
from ..models import Sensor, SensorRecord
from ..schemas import SensorRecordCreateRequest, SensorRecordListParam

router = APIRouter()


@router.get("")
async def list_sensor_record(
    uuid: UUID4 = Query(...),
    days: int = Query(1, ge=1, le=30),
):
    with SessionLocal() as session:
        stmt = select(Sensor).where(Sensor.uuid == uuid)
        sensor: Sensor | None = session.execute(stmt).scalar_one_or_none()
        if not sensor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Sensor not found"
            )
        le = datetime.utcnow()
        ge = le - timedelta(days=days)
        stmt = (
            select(SensorRecord)
            .where(SensorRecord.uuid == sensor.uuid)
            .where(SensorRecord.created_at >= ge)
            .where(SensorRecord.created_at <= le)
            .order_by(SensorRecord.created_at.desc())
            .limit(1500)
        )
        sensor_records = session.execute(stmt).scalars().all()
    return sensor_records


@router.post("")
async def retrieve_sensor(body: SensorRecordCreateRequest = Body(...)):
    with SessionLocal() as session:
        stmt = select(Sensor).where(Sensor.uuid == body.uuid)
        sensor = session.execute(stmt).scalar_one_or_none()
        if not sensor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Sensor not found"
            )
        db_sensor_record = SensorRecord(
            uuid=body.uuid, temperature=body.temperature, humidity=body.humidity
        )
        session.add(db_sensor_record)
        session.commit()
        session.refresh(db_sensor_record)

    return db_sensor_record
