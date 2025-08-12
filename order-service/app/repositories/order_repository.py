from ..core.db import SessionLocal
from sqlalchemy import select
from ..models.order_model import Order

def create_order(order):
    db = SessionLocal()
    db.add(order)
    db.commit()
    db.refresh(order)
    return order