from sqlalchemy import Column, String, Date, DateTime, Float, Integer
from app.core.db import Base

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, autoincrement=True)    
    user_id = Column(Integer, nullable=True)
    total_value = Column(Float, unique=False, nullable=False)
    status = Column(String, nullable=False, default="Pending")
    date = Column(Date, nullable=False)
    start_at = Column(DateTime, nullable=False)
    end_at = Column(DateTime, nullable=True)

    