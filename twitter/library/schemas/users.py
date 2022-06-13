from pydantic import BaseModel, Field
from typing import Optional


class UserUpdate(BaseModel):
    first_name: Optional[str] = Field(None, max_length=60)
    email: str
    username: str
    bio: Optional[str] = None