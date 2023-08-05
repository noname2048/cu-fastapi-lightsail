from datetime import datetime, timedelta

from fastapi import APIRouter, BackgroundTasks, Body, Path, Query, status
from fastapi.exceptions import HTTPException
from pydantic import UUID4
from pytz import timezone
from sqlalchemy import select, text

from ..database import SessionLocal
from ..models import Sensor, SensorRecord
from ..schemas import SensorRecordCreateRequest
from app.ws import publish

kst = timezone("Asia/Seoul")

router = APIRouter()


@router.get("")
async def list_sensor_record(
    uuid: UUID4 = Query(...),
):
    with SessionLocal() as session:
        stmt = select(Sensor).where(Sensor.uuid == uuid)
        sensor: Sensor | None = session.execute(stmt).scalar_one_or_none()
        if not sensor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Sensor not found"
            )
        le = datetime.utcnow()
        ge = le - timedelta(hours=24)
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
async def create_sensor_record(
    bg_task: BackgroundTasks,
    body: SensorRecordCreateRequest = Body(...),
):
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

        bg_task.add_task(
            publish,
            topic=str(db_sensor_record.uuid),
            data={
                "uuid": str(db_sensor_record.uuid),
                "temperature": db_sensor_record.temperature,
                "humidity": db_sensor_record.humidity,
                "created_at": db_sensor_record.created_at.isoformat(),
            },
        )

    return db_sensor_record


@router.get("/query")
async def query_sensor_record(
    uuid: UUID4 = Query(...),
    duration_hours: int = Query(24, selectable=[1, 2, 3, 6, 12, 24, 48]),
    interval_minutes: int = Query(1, selectable=[1, 2, 3, 5, 10, 12, 15, 20, 30]),
):
    sql = text(
        f"""
        select *
        from (
            select *, row_number() over (
                partition by date_trunc('hour', created_at) + interval '{interval_minutes} min' * floor(date_part('minute', created_at) / {interval_minutes})
                order by created_at desc
                ) as rn
            from sensor_record
            where created_at > now() - interval '{duration_hours} hour' and
                uuid = '{uuid}'
            ) tmp
        where rn = 1;
        """
    )

    with SessionLocal() as session:
        statement = select(Sensor).where(Sensor.uuid == uuid)
        sensor: Sensor | None = session.execute(statement).scalar_one_or_none()
        if not sensor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Sensor not found"
            )
        rows = session.execute(sql).all()

    sensor_records: list[SensorRecord] = [row._mapping for row in rows]
    return sensor_records
