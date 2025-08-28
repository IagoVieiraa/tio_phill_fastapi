from pydantic import BaseModel
from datetime import datetime
from typing import List

# schema de cada item do pedido
class OrderItemCreate(BaseModel):
    product_id: int
    product_name: str
    quantity: int
    unit_price: float

# schema para criação do pedido
class OrderCreate(BaseModel):
    items: List[OrderItemCreate] 

# Para resposta da API (o cliente recebe)
class OrderResponse(BaseModel):
    id: int
    user_id: int
    total_value: float
    status: str
    created_at: datetime

    class Config:
        orm_mode = True  # permite usar diretamente objetos SQLAlchemy
