from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Slot, ParkingSession


class SlotRepository:
    """Acceso a datos para Slots (SRP)."""

    def __init__(self, db: Session):
        self.db = db

    def get_free_slot(self) -> Optional[Slot]:
        return self.db.scalar(
            select(Slot).where(Slot.is_occupied.is_(False)).limit(1)
        )

    def get_all(self) -> List[Slot]:
        return self.db.scalars(select(Slot)).all()

    def save(self, slot: Slot):
        self.db.add(slot)

    def refresh_occupied_state(self, slot: Slot):
        active = self.db.scalar(
            select(ParkingSession).where(
                ParkingSession.slot_id == slot.id,
                ParkingSession.check_out_at.is_(None),
            )
        )
        slot.is_occupied = bool(active)
        self.db.add(slot)