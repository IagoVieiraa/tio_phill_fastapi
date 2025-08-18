from fastapi import HTTPException, status
from ..models.menu_model import Menu
from ..schemas.menu_schema import Menu as MenuSchema
from ..repositories import menu_repository
from datetime import  datetime
import httpx


AUTH_SERVICE_URL = "http://localhost:8002"

def create_menu(menu_data: MenuSchema, token_user: str = None):
    try:
        if token_user is None:
            return {"success": False, "body": "Only authenticated users can create a menu object", "status_code": 401}

        date = datetime.now().date()
        created_at = datetime.now()

        user_data = validate_user_token(token_user)
        user_id = user_data.get("user_id")

        if user_data.get("role", "CLIENT") == "CLIENT":
            return {"success": False, "body": "Only internal users can create a menu object", "status_code": 401}

        new_menu = Menu(user_id=user_id, date=date, created_at=created_at)

        created_menu = menu_repository.create_menu(new_menu)
        
        return {"success": True, "body": f"Menu with id {created_menu.id} successfuly", "status_code": 201}
    except Exception as ex:
        print(ex)
        return {"success": False, "body": "Error ocurred in create_menu", "status_code": 500}


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
