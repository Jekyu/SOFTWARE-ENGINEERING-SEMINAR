import math
from app.repositories.tariff_repository import TariffRepository


class TariffService:
    """
    Maneja la lógica de tarifas.
    Cumple OCP: si cambian reglas, se cambia aquí.
    """

    def __init__(self, tariff_repo: TariffRepository):
        self.tariff_repo = tariff_repo

    def get_current_rate(self) -> float:
        tariff = self.tariff_repo.get_active()
        return float(tariff.rate_per_minute) if tariff else 0.05

    def calculate_amount(self, minutes: int) -> float:
        minutes_rounded = max(1, math.ceil(minutes))
        return round(minutes_rounded * self.get_current_rate(), 2)