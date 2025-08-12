from ..models.order_model import Order
from ..repositories import order_repository
from datetime import  datetime

def create_order(**order_data):
    try:
        user_name = order_data.get("user_name", None)
        value = order_data.get("value", 0.0)
        order_date = datetime.now().date()
        start_at = datetime.now()
        
        if user_name == None:
            print("Usuário não registrado")
            ...
        if value == 0.0:
            print("O pedido não pode ser criado com valor = 0")
            return {"success": False, "body": "The order can't be created with value equals zero", "status_code": 400}
        
        new_order = Order(user_name=user_name, value=value, date=order_date, start_at=start_at)

        created_order = order_repository.create_order(new_order)

        return {"success": True, "body": f"Order of {created_order.user_name} registered!", "status_code": 201}
    except Exception as ex:
        print(ex)
        return {"success": False, "body": "Error ocurred in create_order", "status_code": 500}

