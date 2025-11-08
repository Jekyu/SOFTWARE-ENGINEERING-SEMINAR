import os
import sys
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# --- Asegurar que el paquete "app" está en el PYTHONPATH ---

CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app.main import app
from app.db import Base, get_db
from app.models import Slot, Tariff
from app.services.auth_service import get_current_user


@pytest.fixture(scope="session")
def engine():
    """
    Engine SQLite en memoria compartida para todos los tests.
    StaticPool asegura que todas las conexiones vean la misma BD.
    """
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    # Crear todas las tablas una sola vez para este engine de pruebas
    Base.metadata.create_all(bind=engine)
    return engine


@pytest.fixture(scope="function")
def db_session(engine):
    """
    Sesión de BD aislada por test:
    - Usa una conexión sobre el engine compartido.
    - Abre una transacción.
    - Limpia tablas.
    - Inserta datos base (slots + tarifa).
    - Al final hace rollback: ningún test ensucia al siguiente.
    """
    connection = engine.connect()
    transaction = connection.begin()

    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=connection,
    )
    db = TestingSessionLocal()

    # Limpiar todas las tablas antes de sembrar datos
    for table in reversed(Base.metadata.sorted_tables):
        db.execute(table.delete())

    # Semilla: slots disponibles
    for code in ["A01", "A02", "A03"]:
        db.add(Slot(code=code, is_occupied=False))

    # Semilla: una tarifa activa
    db.add(Tariff(rate_per_minute=0.05, active=True))

    db.commit()

    try:
        yield db
    finally:
        db.close()
        transaction.rollback()
        connection.close()


@pytest.fixture(scope="function")
def client(db_session):
    """
    TestClient configurado para:
    - Usar la db_session de pruebas (override de get_db).
    - Usar un usuario simulado siempre válido (override de get_current_user).
    """

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    def override_get_current_user():
        return {"sub": "test@local", "roles": ["TEST"]}

    app.dependency_overrides[get_current_user] = override_get_current_user

    with TestClient(app) as c:
        yield c

    # Limpiar overrides después de cada test
    app.dependency_overrides.clear()