from typing import List
from app.repositories.slot_repository import SlotRepository
from app.schemas import SlotOut


class SlotService:
    """Lógica de negocio de slots."""

    def __init__(self, slot_repo: SlotRepository):
        self.slot_repo = slot_repo

    def get_free_slot(self):
        return self.slot_repo.get_free_slot()

    def get_slots_with_status(self) -> List[SlotOut]:
        slots = self.slot_repo.get_all()
        result: List[SlotOut] = []
        for s in slots:
            active = next((ses for ses in s.sessions if ses.check_out_at is None), None)
            result.append(
                SlotOut(
                    code=s.code,
                    occupied=s.is_occupied,
                    plate=active.plate if active else None,
                )
            )
        return result