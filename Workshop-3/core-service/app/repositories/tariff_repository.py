from typing import Optional
from sqlalchemy import select, desc
from sqlalchemy.orm import Session

from app.models import Tariff


class TariffRepository:
    """Acceso a datos de Tariff."""

    def __init__(self, db: Session):
        self.db = db

    def get_active(self) -> Optional[Tariff]:
        stmt = (
            select(Tariff)
            .where(Tariff.active.is_(True))
            .order_by(desc(Tariff.created_at))
            .limit(1)
        )
        return self.db.scalar(stmt)