from sqlalchemy.orm import Session
from ..repositories import product_repository
from ..schemas.product_schema import ProductCreate

def create_product(db: Session, product: ProductCreate):
    db_product = product_repository.get_product_by_name(db, name=product.name)
    if db_product:
        return {"status_code": 400, "message": "Product already registered"}
    
    new_product = product_repository.create_product(db=db, product=product)
    return {"status_code": 201, "message": "Product created successfully", "data": {"product_id": new_product.id}}

def get_all_products(db: Session):
    products = product_repository.get_products(db)
    return {"status_code": 200, "data": products}