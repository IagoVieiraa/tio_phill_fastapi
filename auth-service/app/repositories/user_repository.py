from app.core.db import SessionLocal

def create_user(new_user):
    db = SessionLocal()
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user