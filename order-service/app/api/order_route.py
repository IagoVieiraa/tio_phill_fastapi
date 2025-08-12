from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from ..services import order_service
from ..schemas.order_schema import Order

router = APIRouter()

@router.post("/orders/create")
def register_order(order_data: dict):
    result = order_service.create_order(**order_data)
    return JSONResponse(
        content=result,
        status_code=result["status_code"]
    )