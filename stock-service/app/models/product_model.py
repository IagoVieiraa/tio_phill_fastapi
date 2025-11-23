from sqlalchemy import Column, String, Float, Integer
from app.core.db import Base

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)