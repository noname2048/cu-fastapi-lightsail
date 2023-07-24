from datetime import datetime
from typing import Optional

from pydantic import UUID4, BaseModel


class SensorCreateRequest(BaseModel):
    name: str


class Sensor(BaseModel):
    uuid: str
    name: str
    created_at: datetime


class SensorRecordCreateRequest(BaseModel):
    uuid: UUID4
    temperature: float
    humidity: float
    created_at: datetime


class SensorRecordListParam(BaseModel):
    uuid: UUID4
    days: Optional[int] = 1
