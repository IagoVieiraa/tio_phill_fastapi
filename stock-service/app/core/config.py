from pydantic_settings import BaseSettings
from typing import ClassVar
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: ClassVar[str] = os.getenv("DATABASE_URL")
settings = Settings()
