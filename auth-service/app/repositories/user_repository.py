from ..core.db import SessionLocal
from sqlalchemy import select
from ..models.user_model import User

def create_user(new_user):
    db = SessionLocal()
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user_by_email(email: str) -> bool:
    db = SessionLocal()
    stmt = select(User).where(User.email == email)
    result = db.execute(stmt).scalar_one_or_none()
    return result