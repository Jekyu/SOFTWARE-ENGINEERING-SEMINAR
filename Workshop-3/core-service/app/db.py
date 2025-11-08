from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from .config import get_settings

settings = get_settings()


class Base(DeclarativeBase):
    """Base ORM para todos los modelos."""
    pass


engine = create_engine(settings.DATABASE_URL, echo=False, future=True)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    future=True,
)


def get_db():
    """Dependencia de FastAPI: sesión por request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()