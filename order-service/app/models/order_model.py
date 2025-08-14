from sqlalchemy import Column, String, Date, DateTime, Float, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
from uuid import uuid4

Base = declarative_base()

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, autoincrement=True)    
    user_id = Column(Integer, unique=False, nullable=True)
    total_value = Column(Float, unique=False, nullable=False)
    status = Column(String, nullable=False, default="Pending")
    
    date = Column(Date, nullable=False)
    start_at = Column(DateTime, nullable=False)
    end_at = Column(DateTime, nullable=True)

    