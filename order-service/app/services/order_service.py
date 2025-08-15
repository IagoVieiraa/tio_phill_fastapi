from fastapi import HTTPException, status
from ..models.order_model import Order
from ..repositories import order_repository
from datetime import  datetime
import httpx


AUTH_SERVICE_URL = "http://localhost:8002"

def create_order(order_data: dict, token_user: str = None):
    try:
        value = order_data.get("value", 0.0)
        status = order_data.get("status")
        order_date = datetime.now().date()
        start_at = datetime.now()
        user_id = None

        if token_user is not None:
            user_id = validate_user_token(token_user)
        if user_id == None:
            print("Usuário não registrado")
            ...
        new_order = Order(user_id=user_id, total_value=value, status=status, date=order_date, start_at=start_at)

        created_order = order_repository.create_order(new_order)

        return {"success": True, "body": f"Order with id {created_order.id} registered!", "status_code": 201}
    except Exception as ex:
        print(ex)
        return {"success": False, "body": "Error ocurred in create_order", "status_code": 500}


def validate_user_token(token: str) -> int:
    try:
        response = httpx.get(
            f"{AUTH_SERVICE_URL}/auth/users/check-token",
            headers={"Authorization": f"Bearer {token}"}
        )
        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuário não autenticado"
            )
        return response.json().get("body", {}).get("id")
    except  Exception as ex:
        return None
