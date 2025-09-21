from fastapi import APIRouter, HTTPException, status, Header
from fastapi.responses import JSONResponse
from ..services import user_service
from ..schemas.auth_schema import Login, Token
from ..schemas.user_schema import User
from ..types.response import Response
router = APIRouter()

@router.post("/users/create")
def register_user(user_credentials: User):
    result: Response = user_service.create_user(user_credentials)
    return JSONResponse(
        content=result.__dict__,
        status_code=result.status_code
    )

@router.post("/users/login", response_model=Token)
def login_endpoint(credentials: Login):
    token = user_service.login(credentials)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")
    return {"access_token": token, "token_type": "bearer"}

@router.get("/users/check-token")
def get_user_authenticate(authorization: str = Header(...)):
    result = user_service.check_token(authorization)    
    return JSONResponse(
        content=result,
        status_code=result["status_code"]
    )