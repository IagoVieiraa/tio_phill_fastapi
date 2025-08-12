from pydantic import BaseModel

class Order(BaseModel):
    user_name: set
    date: str
    value: float
    start_at: str
    end_at: str
