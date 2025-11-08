from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db_session, get_auth_user
from app.repositories.slot_repository import SlotRepository
from app.services.slot_service import SlotService
from app.schemas import SlotOut

router = APIRouter(prefix="/slots", tags=["slots"])

@router.get("", response_model=list[SlotOut])
def list_slots(
    db: Session = Depends(get_db_session),
    user=Depends(get_auth_user),
):
    service = SlotService(SlotRepository(db))
    return service.get_slots_with_status()