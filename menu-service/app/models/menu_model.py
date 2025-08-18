from sqlalchemy import Column, String, Date, DateTime, Float, Integer
from app.core.db import Base

class Menu(Base):
    __tablename__ = "menu"
    id = Column(Integer, primary_key=True, autoincrement=True)    
    user_id = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    created_at = Column(DateTime, nullable=False)
    end_at = Column(DateTime, nullable=True)
