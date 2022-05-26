from ast import Return
from fastapi import APIRouter
from library.schemas.register import UserCreate, UserPublic
import bcrypt
from passlib.context import CryptContext
from models.users import User
import random
from library.security.otp import otp_manager


router = APIRouter(prefix="/auth")
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


@router.post("/register/", response_model=UserPublic) ##refer to users.py
async def register(data: UserCreate):
    ##Create account.
    hashed_password = pwd_context.hash(data.password)
    created_user = await User.create(
        **data.dict(exclude_unset=True,exclude={'password'}),
    hashed_password = hashed_password
    )
    ##endpoint for email verification(construct email that sends verification token:import random)
    token= otp_manager.create_otp(str(created_user.id))
    print(f'sending verification token: {token}')
    return created_user
