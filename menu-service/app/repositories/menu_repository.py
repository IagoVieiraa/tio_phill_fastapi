from ..core.db import SessionLocal
from sqlalchemy import select
from ..models.menu_model import Menu

def create_menu(menu):
    db = SessionLocal()
    db.add(menu)
    db.commit()
    db.refresh(menu)
    return menu