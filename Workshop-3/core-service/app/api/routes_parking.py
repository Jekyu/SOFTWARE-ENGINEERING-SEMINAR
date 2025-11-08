from fastapi import APIRouter, Depends, Query, Body
from sqlalchemy.orm import Session

from app.api.deps import get_db_session, get_auth_user
from app.schemas import (
    EntryResponse,
    ExitResponse,
    SessionsListResponse,
    StatsOverviewResponse,
)
from app.services.parking_service import ParkingService

router = APIRouter(tags=["parking"])


@router.post("/entries", response_model=EntryResponse)
def create_entry(
    # 👇 MUY IMPORTANTE: embed=True => espera JSON { "plate": "ABC123" }
    plate: str = Body(..., embed=True),
    db: Session = Depends(get_db_session),
    user=Depends(get_auth_user),
):
    """
    Registra la entrada de un vehículo.
    Request esperado:
    {
      "plate": "ABC123"
    }
    """
    service = ParkingService(db)
    return service.register_entry(plate)


@router.post("/exits", response_model=ExitResponse)
def create_exit(
    plate: str = Body(..., embed=True),
    db: Session = Depends(get_db_session),
    user=Depends(get_auth_user),
):
    """
    Registra la salida de un vehículo y calcula el cobro.
    Request esperado:
    {
      "plate": "ABC123"
    }
    """
    service = ParkingService(db)
    return service.register_exit(plate)


@router.get("/sessions", response_model=SessionsListResponse)
def get_sessions(
    limit: int = Query(5, ge=1, le=100),
    db: Session = Depends(get_db_session),
    user=Depends(get_auth_user),
):
    """
    Lista sesiones recientes para el dashboard.
    """
    service = ParkingService(db)
    return service.list_recent_sessions(limit=limit)


@router.get("/stats/overview", response_model=StatsOverviewResponse)
def stats_overview(
    db: Session = Depends(get_db_session),
    user=Depends(get_auth_user),
):
    """
    Resumen de ocupación para el dashboard.
    """
    service = ParkingService(db)
    return service.get_overview_stats()