from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    access: str
    refresh: str

class UserInfo(BaseModel):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str | None = None
    created_by: str | None = None




