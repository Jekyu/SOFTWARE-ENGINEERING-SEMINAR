from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.parking_repository import ParkingRepository
from app.repositories.slot_repository import SlotRepository
from app.repositories.tariff_repository import TariffRepository
from app.schemas import (
    EntryResponse,
    ExitResponse,
    SessionsListResponse,
    ParkingSessionOut,
    StatsOverviewResponse,
)
from app.models import ParkingSession
from .tariff_service import TariffService
from .slot_service import SlotService


class ParkingService:
    """
    Lógica principal del core-service:
    - Registrar entrada
    - Registrar salida con cobro
    - Listar sesiones recientes
    - Overview para dashboard
    """

    def __init__(self, db: Session):
        self.db = db
        self.parking_repo = ParkingRepository(db)
        self.slot_repo = SlotRepository(db)
        self.tariff_service = TariffService(TariffRepository(db))
        self.slot_service = SlotService(self.slot_repo)

    # ---------- ENTRADA ----------

    def register_entry(self, plate: str) -> EntryResponse:
        plate = plate.upper().strip()

        if not plate:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="plate is required",
            )

        if self.parking_repo.get_active_by_plate(plate):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Vehicle is already inside.",
            )

        slot = self.slot_service.get_free_slot()
        if not slot:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No available slots.",
            )

        session = ParkingSession(plate=plate, slot=slot)
        self.parking_repo.create(session)
        slot.is_occupied = True
        self.slot_repo.save(slot)

        self.db.commit()
        self.db.refresh(session)

        return EntryResponse(
            session_id=session.id,
            plate=session.plate,
            slot_code=slot.code,
            check_in_at=session.check_in_at,
        )

    # ---------- SALIDA ----------

    def register_exit(self, plate: str) -> ExitResponse:
        plate = plate.upper().strip()

        if not plate:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="plate is required",
            )

        session = self.parking_repo.get_active_by_plate(plate)
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No active session for this plate.",
            )

        now = datetime.utcnow()
        diff = now - session.check_in_at
        minutes = int(diff.total_seconds() / 60)
        if minutes <= 0:
            minutes = 1

        amount = self.tariff_service.calculate_amount(minutes)
        rate = self.tariff_service.get_current_rate()

        session.check_out_at = now
        session.minutes_total = minutes
        session.rate_per_minute = rate
        session.amount_total = amount

        self.slot_repo.refresh_occupied_state(session.slot)

        self.db.commit()
        self.db.refresh(session)

        return ExitResponse(
            session_id=session.id,
            plate=session.plate,
            minutes=minutes,
            amount=float(amount),
            check_in_at=session.check_in_at,
            check_out_at=session.check_out_at,
        )

    # ---------- SESIONES ----------

    def list_recent_sessions(self, limit: int = 5) -> SessionsListResponse:
        sessions = self.parking_repo.list_recent(limit)
        items = [
            ParkingSessionOut(
                id=s.id,
                plate=s.plate,
                slot_code=s.slot.code if s.slot else "",
                check_in_at=s.check_in_at,
                check_out_at=s.check_out_at,
            )
            for s in sessions
        ]
        return SessionsListResponse(items=items)

    # ---------- OVERVIEW ----------

    def get_overview_stats(self) -> StatsOverviewResponse:
        slots = self.slot_repo.get_all()
        total = len(slots)
        occupied = sum(1 for s in slots if s.is_occupied)
        free = total - occupied if total > 0 else 0

        occupancy = (occupied / total * 100) if total > 0 else 0.0
        rate = self.tariff_service.get_current_rate()

        return StatsOverviewResponse(
            occupied=occupied,
            free=free,
            activeVehicles=occupied,
            currentRatePerMinute=rate,
            occupancyPercent=round(occupancy, 1),
        )