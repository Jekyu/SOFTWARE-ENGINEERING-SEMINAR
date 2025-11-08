from datetime import datetime
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models import ParkingSession


class ReportService:
    """Reportes sencillos para el taller."""

    def __init__(self, db: Session):
        self.db = db

    def count_sessions_between(self, start: datetime, end: datetime) -> int:
        stmt = select(func.count(ParkingSession.id)).where(
            ParkingSession.check_in_at >= start,
            ParkingSession.check_in_at <= end,
        )
        return self.db.scalar(stmt) or 0