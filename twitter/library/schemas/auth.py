from datetime import datetime
from pydantic import BaseModel
from datetime import datetime

from twitter.library.schemas.register import UserPublic

class loginschema(BaseModel):
    username_or_email: str
    password: str

class JWTSchemas(BaseModel):
    user_id: str
    expire: datetime

class AuthResponse(BaseModel):
    user: UserPublic
    token: str