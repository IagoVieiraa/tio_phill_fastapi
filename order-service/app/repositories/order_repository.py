from ..core.db import SessionLocal
from sqlalchemy import select
from ..models.order_model import Order

def create_order(order):
    db = SessionLocal()
    db.add(order)
    db.commit()
    db.refresh(order)
    return order

def create_order_item(order_item, order_id):
    db = SessionLocal()
    order_item.order_id = order_id
    db.add(order_item)
    db.commit()
    db.refresh(order_item)
    return order_item

def update_order(order):
    db = SessionLocal()
    db.merge(order)
    db.commit()
    db.refresh(order)
    return order
