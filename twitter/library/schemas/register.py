from typing import Optional
from pydantic import BaseModel,EmailStr, Field

##we defined the kind of data we want to get from the user(client/frontend) using pydantic basemodel
class UserCreate(BaseModel):
    username: str = Field(..., max_length =40)
    email: EmailStr
    first_name:str = Field(..., max_length=60)
    last_name:Optional[str] = Field(None, max_length=60)
    phone:Optional[str] = Field(None, max_length=15)
    day_of_birth:Optional[str] = Field(None, max_length=15)
    month_of_birth:Optional[str] = Field(None, max_length=15)
    year_of_birth:Optional[str] = Field(None, max_length=15)
    password:str=Field(..., min_length=8, max_length=1500)