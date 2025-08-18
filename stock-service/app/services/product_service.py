import json
from fastapi import HTTPException, status
from ..models.order_model import Order
from ..models.order_item import OrderItem
from ..schemas.order_schema import OrderCreate as OrderCreateSchema
from ..repositories import order_repository
from datetime import  datetime
import httpx


AUTH_SERVICE_URL = "http://localhost:8002"
STOCK_SERVICE_URL = "http://localhost:8004"

def create_order(order_data: OrderCreateSchema, token_user: str = None):
    try:
        total_price = 0
        status = "pending"
        order_date = datetime.now().date()
        start_at = datetime.now()
        user_id = None
        order_items = []

        if token_user is not None:
            user_data = validate_user_token(token_user)
            user_id = user_data.get("user_id")
        
        new_order = Order(user_id=user_id, total_value=total_price, status=status, date=order_date, start_at=start_at)
        created_order = order_repository.create_order(new_order)

        items = order_data.items       
        for item in items:
            order_item = OrderItem()
            order_item.order_id = created_order.id
            order_item.product_id = item.product_id
            order_item.quantity = item.quantity
            order_item.unit_price = item.unit_price
            order_item.total_price += item.unit_price * item.quantity
            created_order_item = order_repository.create_order_item(order_item)
            order_items.append(created_order_item)
        
        if len(order_items) > 0:
            down_items_from_stock(order_items)
    except Exception as ex:
        print(ex)
        return {"success": False, "body": "Error ocurred in create_order", "status_code": 500}

def validate_user_token(token: str) -> dict:
    try:
        response = httpx.get(
            f"{AUTH_SERVICE_URL}/auth/users/check-token",
            headers={"Authorization": token}
        )
        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuário não autenticado"
            )
        user_data = response.json().get("body")
        return user_data
    except  Exception as ex:
        return None

def down_items_from_stock(order_items_created: list[dict]) -> bool:
    payload = json.loads(order_items_created)
    response = httpx.post(
        f"{STOCK_SERVICE_URL}/ingredient/down",
        data=payload
    )
    if response.status_code != 200:
        return False
    
    if response.json().get("success") == True:
        return True
    
    else:
        return False
