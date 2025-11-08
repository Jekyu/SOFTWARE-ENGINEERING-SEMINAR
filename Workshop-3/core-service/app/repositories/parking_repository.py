from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models import ParkingSession


class ParkingRepository:
    """Acceso a datos para sesiones de parqueo."""

    def __init__(self, db: Session):
        self.db = db

    def get_active_by_plate(self, plate: str) -> Optional[ParkingSession]:
        stmt = (
            select(ParkingSession)
            .where(
                ParkingSession.plate == plate,
                ParkingSession.check_out_at.is_(None),
            )
            .options(joinedload(ParkingSession.slot))
            .limit(1)
        )
        return self.db.scalar(stmt)

    def create(self, session: ParkingSession) -> ParkingSession:
        self.db.add(session)
        self.db.flush()
        return session

    def list_recent(self, limit: int = 5) -> List[ParkingSession]:
        stmt = (
            select(ParkingSession)
            .options(joinedload(ParkingSession.slot))
            .order_by(ParkingSession.check_in_at.desc())
            .limit(limit)
        )
        return self.db.scalars(stmt).all()