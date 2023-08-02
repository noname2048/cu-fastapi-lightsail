from fastapi import APIRouter, Body, Path, Query
from pydantic import UUID4
from sqlalchemy import select, text

from ..database import SessionLocal
from ..models import Sensor
from ..schemas import SensorCreateRequest, SensorWithLastResponse

router = APIRouter()


@router.get("")
async def list_sensor():
    with SessionLocal() as session:
        stmt = select(Sensor)
        sensors = session.execute(stmt).scalars().all()
    return sensors


@router.get("/last", response_model=list[SensorWithLastResponse])
async def list_sensor_with_last_record():
    with SessionLocal() as session:
        session.query(Sensor)
        query = text(
            """
            select s.*, x.temperature, x.humidity, x.created_at as last
            from sensor s
                left join
                (
                    select *
                    from (
                        select *,
                            row_number() over (
                                partition by uuid
                                order by created_at desc
                            ) as rank
                        from sensor_record
                    ) t
                    where rank = 1
                    order by created_at desc
                ) x on s.uuid = x.uuid
            order by s.created_at asc;
            """
        )
        rows = session.execute(query).all()
        results = [row._mapping for row in rows]
    return results


@router.get("/uuid/{uuid}")
async def retrieve_sensor(uuid: UUID4 = Path(...)):
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
