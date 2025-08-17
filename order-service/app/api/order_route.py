from fastapi import APIRouter, HTTPException, Header, status
from fastapi.responses import JSONResponse
from ..services import order_service
from ..schemas.order_schema import Order

router = APIRouter()

@router.post("/create")
def create_order(order_data: dict, authorization: str = Header(None)):
    # token = order_data.get("user_token")
    result = order_service.create_order(order_data, authorization)

    return JSONResponse(
        content=result,
        status_code=result["status_code"]
    )
