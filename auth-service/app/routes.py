from fastapi import APIRouter
from .schemas import UserCreate
from .models import User
from .db import SessionLocal
from .utils import hash_password

router = APIRouter()

@router.post("/register")
def register_user(user: UserCreate):
    db = SessionLocal()
    hashed_pw = hash_password(user.password)
    new_user = User(email=user.email, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    return {"message": "User Registered"}