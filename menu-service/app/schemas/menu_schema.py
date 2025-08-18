from pydantic import BaseModel

class Menu(BaseModel):
    user_id: int
    date: str
    created_at: str
    endt_at: str
