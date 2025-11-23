from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from ..services import product_service
from ..schemas.product_schema import ProductCreate
from ..core.db import get_db

router = APIRouter()

@router.post("/products/create")
def create_product(product_data: ProductCreate, db: Session = Depends(get_db)):
    result = product_service.create_product(db, product_data)
    return JSONResponse(
        content=result,
        status_code=result["status_code"]
    )

@router.get("/products")
def get_all_products_endpoint(db: Session = Depends(get_db)):
    result = product_service.get_all_products(db)
    return JSONResponse(
        content=result,
        status_code=result["status_code"]
    )