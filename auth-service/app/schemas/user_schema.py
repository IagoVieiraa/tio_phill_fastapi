from pydantic import BaseModel, EmailStr, constr
from typing import Annotated

class User(BaseModel):
    email: str
    password: str
    role: Annotated[str, constr(to_upper=True)]