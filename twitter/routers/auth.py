from ast import Return
from fastapi import APIRouter
from library.schemas.register import UserCreate
import bcrypt
from passlib.context import CryptContext
from models.users import User

router = APIRouter(prefix="/auth")
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


@router.post("/register/")
async def register(data: UserCreate):
    ##Create account.
    password_hash = pwd_context.hash(data.password)
    # created_user = await User.Create(data.dict(exclude_unset=True,exclude={'password'}))
    return {"detail": "hello", **data.dict()}
