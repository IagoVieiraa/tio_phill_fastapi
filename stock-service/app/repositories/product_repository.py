from sqlalchemy.orm import Session
from ..models.product_model import Product
from ..schemas.product_schema import ProductCreate

def get_product_by_name(db: Session, name: str):
    return db.query(Product).filter(Product.name == name).first()

def create_product(db: Session, product: ProductCreate):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Product).offset(skip).limit(limit).all()

def update_product_quantity(db: Session, product_id: int, quantity: int):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product:
        db_product.quantity = quantity
        db.commit()
        db.refresh(db_product)
    return db_product
