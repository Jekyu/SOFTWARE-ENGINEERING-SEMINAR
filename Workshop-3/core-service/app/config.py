import os
from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    # Core-service usa PostgreSQL
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/parking_db"

    # JWT emitido por AUTH-SERVICE (Java) — aquí SOLO se valida
    JWT_SECRET: str = "SUPER_SECRET_CHANGE_ME"
    JWT_ALGORITHM: str = "HS256"
    JWT_ISSUER: str = "parking-auth-service"

    # Prefijo usado por el Web UI
    API_PREFIX: str = "/api/core"

    # Para desarrollo: si True, se salta la validación JWT (solo DEV)
    DISABLE_AUTH: bool = True

    # Origen permitido para el frontend
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:8081"]

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings()