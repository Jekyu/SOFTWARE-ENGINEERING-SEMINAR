from datetime import datetime
from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .db import Base


class Slot(Base):
    """
    Espacio de parqueadero.
    Ej: "A01", "B10".
    """
    __tablename__ = "slots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    code: Mapped[str] = mapped_column(String(10), unique=True, index=True)
    is_occupied: Mapped[bool] = mapped_column(Boolean, default=False)

    # Una plaza puede tener muchas sesiones históricas
    sessions: Mapped[list["ParkingSession"]] = relationship(
        back_populates="slot", cascade="all, delete-orphan"
    )


class ParkingSession(Base):
    """
    Estancia de un vehículo:
    - check_in_at cuando entra
    - check_out_at cuando sale
    - minutos, tarifa y monto al cerrar
    """
    __tablename__ = "parking_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    plate: Mapped[str] = mapped_column(String(16), index=True)

    slot_id: Mapped[int] = mapped_column(ForeignKey("slots.id"), nullable=False)
    slot: Mapped["Slot"] = relationship(back_populates="sessions")

    check_in_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    check_out_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    minutes_total: Mapped[int | None] = mapped_column(Integer, nullable=True)
    rate_per_minute: Mapped[Numeric | None] = mapped_column(Numeric(10, 4))
    amount_total: Mapped[Numeric | None] = mapped_column(Numeric(10, 2))


class Tariff(Base):
    """
    Tarifa por minuto.
    Para el proyecto: se toma la última activa.
    """
    __tablename__ = "tariffs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    rate_per_minute: Mapped[Numeric] = mapped_column(Numeric(10, 4))
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)