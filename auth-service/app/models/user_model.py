from sqlalchemy import Column, String, Integer, Enum
from app.core.db import Base
import enum
class UserRole(enum.Enum):
    INTERNAL = "INTERNAL"
    CLIENT = "CLIENT"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False)