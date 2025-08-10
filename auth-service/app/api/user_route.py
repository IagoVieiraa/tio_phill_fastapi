from fastapi import APIRouter
from fastapi.responses import JSONResponse
from ..services import user_service
from ..schemas.user_schema import UserCreate

router = APIRouter()

@router.post("/users/create")
def register_user(user: UserCreate):
    result = user_service.service_create_user(**dict(user))
    return JSONResponse(
        content=result,
        status_code=result["status_code"]
    )