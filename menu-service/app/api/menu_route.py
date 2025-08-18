from fastapi import APIRouter, HTTPException, Header, status
from fastapi.responses import JSONResponse
from ..services import menu_service
from ..schemas.menu_schema import Menu

router = APIRouter()

@router.post("/create")
def create_menu(menu_data: Menu, authorization: str = Header(None)):
    result = menu_service.create_menu(menu_data, authorization)

    return JSONResponse(
        content=result,
        status_code=result["status_code"]
    )
