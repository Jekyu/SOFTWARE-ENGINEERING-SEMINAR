from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db_session, get_auth_user
from app.services.report_service import ReportService

router = APIRouter(prefix="/reports", tags=["reports"])

@router.get("/count")
def count_sessions(
    start: datetime,
    end: datetime,
    db: Session = Depends(get_db_session),
    user=Depends(get_auth_user),
):
    return {"count": ReportService(db).count_sessions_between(start, end)}