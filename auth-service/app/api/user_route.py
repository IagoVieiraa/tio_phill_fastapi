from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from ..services import user_service
from ..schemas.auth_schema import Login, Token
from ..schemas.user_schema import UserCreate

router = APIRouter()

@router.post("/users/create")
def register_user(user_credentials: dict):
    result = user_service.create_user(**user_credentials)
    return JSONResponse(
        content=result,
        status_code=result["status_code"]
    )

@router.post("/users/login", response_model=Token)
def login_endpoint(credentials: dict):
    token = user_service.login(**credentials)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")
    return {"access_token": token, "token_type": "bearer"}