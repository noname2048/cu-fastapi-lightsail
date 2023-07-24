from datetime import datetime
from uuid import uuid4

from sqlalchemy import UUID, Boolean, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class Sensor(Base):
    __tablename__ = "sensor"

    uuid: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(30))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now
    )
    is_active = mapped_column(Boolean, default=True)

    sensor_record: Mapped[list["SensorRecord"]] = relationship()


class SensorRecord(Base):
    __tablename__ = "sensor_record"

    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[UUID] = mapped_column(ForeignKey("sensor.uuid"))
    temperature: Mapped[float] = mapped_column(Float)
    humidity: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    sensor: Mapped["Sensor"] = relationship(back_populates="sensor_record")
