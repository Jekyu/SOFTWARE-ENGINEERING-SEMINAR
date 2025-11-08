from fastapi import Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.services.auth_service import get_current_user


def get_db_session(db: Session = Depends(get_db)):
    return db


def get_auth_user(user=Depends(get_current_user)):
    return user