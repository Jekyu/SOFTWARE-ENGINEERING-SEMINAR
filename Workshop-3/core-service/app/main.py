from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.db import Base, engine
from app.api import routes_health, routes_slots, routes_parking, routes_reports

settings = get_settings()

app = FastAPI(
    title="Parking Core Service",
    version="1.0.0",
)

# CORS para el Web UI
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar rutas con el prefijo /api/core
app.include_router(routes_health.router, prefix=settings.API_PREFIX)
app.include_router(routes_slots.router, prefix=settings.API_PREFIX)
app.include_router(routes_parking.router, prefix=settings.API_PREFIX)
app.include_router(routes_reports.router, prefix=settings.API_PREFIX)


def init_db():
    """
    Crear tablas en la base configurada (PostgreSQL en desarrollo).
    Se llama sólo cuando tú lo decidas, no al importar el módulo.
    """
    Base.metadata.create_all(bind=engine)


# OPCIONAL:
# Si quieres que en ejecución normal cree las tablas automáticamente,
# puedes activar esto solo cuando no estás en tests:
if __name__ == "__main__":
    # Solo se ejecuta si corres: python -m app.main
    init_db()