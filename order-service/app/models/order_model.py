from sqlalchemy import Column, String, Date, DateTime, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
from uuid import uuid4

Base = declarative_base()

class Order(Base):
    __tablename__ = "orders"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_name = Column(String, unique=False, nullable=False)
    value = Column(Float, unique=False, nullable=False)
    date = Column(Date, nullable=False)
    start_at = Column(DateTime, nullable=False)
    end_at = Column(DateTime, nullable=True)

    