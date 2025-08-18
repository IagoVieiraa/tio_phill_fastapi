from sqlalchemy import Column, String, Float, ForeignKey, Integer
from app.core.db import Base 
from .menu_model import Menu


class MenuItem(Base):
    __tablename__ = "menu_item"
    id = Column(Integer, primary_key=True, autoincrement=True)    
    menu_id = Column(Integer, ForeignKey("menu.id"), nullable=False)
    item_name = Column(String, nullable=False)
    unit_price = Column(Float, nullable=False)
