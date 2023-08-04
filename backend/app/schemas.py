from datetime import datetime
from typing import Optional

from pydantic import UUID4, BaseModel, ConfigDict


class SensorCreateRequest(BaseModel):
    name: str
    alias: Optional[str]


class Sensor(BaseModel):
    uuid: str
    name: str
    alias: Optional[str]
    created_at: datetime


class SensorRecordCreateRequest(BaseModel):
    uuid: UUID4
    temperature: float
    humidity: float


class SensorWithLastResponse(Sensor):
    uuid: UUID4
    alias: Optional[str]
    temperature: Optional[float]
    humidity: Optional[float]
    last: Optional[datetime]

    model_config: ConfigDict = ConfigDict(extra="ignore")
