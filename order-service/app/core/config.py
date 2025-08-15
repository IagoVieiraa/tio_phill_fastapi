from pydantic_settings import BaseSettings
from typing import ClassVar
import os
from dotenv import load_dotenv

load_dotenv()  # Carrega variáveis do .env

class Settings(BaseSettings):
    SECRET_KEY: str = "sua_chave_super_segura"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: ClassVar[str] = os.getenv("DATABASE_URL")
settings = Settings()
