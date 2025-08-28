from fastapi import APIRouter, HTTPException, Header, status
from fastapi.responses import JSONResponse
from ..services import order_service
from ..schemas.order_schema import OrderCreate, OrderResponse

router = APIRouter()

@router.post("/create", response_model=OrderResponse)
def create_order(order_data: OrderCreate, authorization: str = Header(None)):
    result = order_service.create_order(order_data, authorization)

    return JSONResponse(
        content=result,
        status_code=result["status_code"]
    )
