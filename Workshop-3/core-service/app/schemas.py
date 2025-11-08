from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


# ---------- Requests ----------

class EntryRequest(BaseModel):
    plate: str


class ExitRequest(BaseModel):
    plate: str


# ---------- Responses ----------

class EntryResponse(BaseModel):
    session_id: int
    plate: str
    slot_code: str
    check_in_at: datetime


class ExitResponse(BaseModel):
    session_id: int
    plate: str
    minutes: int
    amount: float
    check_in_at: datetime
    check_out_at: datetime


class SlotOut(BaseModel):
    code: str
    occupied: bool
    plate: Optional[str] = None


class ParkingSessionOut(BaseModel):
    id: int
    plate: str
    slot_code: str
    check_in_at: datetime
    check_out_at: Optional[datetime] = None


class SessionsListResponse(BaseModel):
    items: List[ParkingSessionOut]


class StatsOverviewResponse(BaseModel):
    occupied: int
    free: int
    activeVehicles: int
    currentRatePerMinute: float
    occupancyPercent: float