from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..models.order_model import Base
import os
from pathlib import Path
from .config import settings

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_URL = settings.DATABASE_URL

engine = create_engine(DATABASE_URL, connect_args={})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)