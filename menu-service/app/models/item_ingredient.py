from sqlalchemy import Column, String, Float, ForeignKey, Integer
from app.core.db import Base 
from .menu_item import MenuItem


class ItemIngredient(Base):
    __tablename__ = "item_ingredient"
    id = Column(Integer, primary_key=True, autoincrement=True)    
    item_id = Column(Integer, ForeignKey("menu_item.id"), nullable=False)
    ingredient_id = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
