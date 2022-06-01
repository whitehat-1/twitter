
from http.client import HTTPException
from fastapi import APIRouter, Path, HTTPException, status
from library.schemas.register import UserCreate, UserPublic
import bcrypt
from passlib.context import CryptContext
from models.users import User
import random
from jose import jwt
from library.security.otp import otp_manager
from uuid import UUID
from datetime import datetime, timedelta, timezone
from config import SECRET_KEY, ALGORITHM

from twitter.library.schemas.auth import AuthResponse, loginschema, JWTSchemas


router = APIRouter(prefix="/auth")
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


@router.post("/register/", response_model=UserPublic) ##refer to users.py
async def register(data: UserCreate):
    ##Create account.

    email_exists = await User.filter(email=data.email).exists()
    username_exists = await User.filter(username=data.username).exists()
    if email_exists or username_exists:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Username or Email already exists"
            )

    hashed_password = pwd_context.hash(data.password)
    created_user = await User.create(
        **data.dict(exclude_unset=True,exclude={'password'}),
    hashed_password = hashed_password
    )
    ##endpoint for email verification(construct email that sends verification token:import random)
    token= otp_manager.create_otp(str(created_user.id))
    print(f'sending verification token: {token}')
    return created_user
 


@router.get("/verify-account/{otp}", response_model=UserPublic)
async def verify(otp: str = Path(...)):
    user_id = otp_manager.get_otp_user(otp)
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid OTP")

    await User.get(id=UUID(user_id)).update(
        email_verified= True
    )
    return  await User.get(id=UUID(user_id)) 



@router.post("/login/", response_model=str)
async def login(data: loginschema):
    ##handle user login
    user = await User.get_or_none(email=data.username_or_email)
    
    #Extract User.
    if user is None:
        user = await User.get_or_none(username=data.username_or_email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Incorrect username or email"
        )
    #Check password.
    hashed_password = user.hashed_password
    is_valid_password: bool = pwd_context.verify(data.password, hashed_password)
    if is_valid_password is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Incorrect password"
            )

    #Generate JWT token.

    jwt_data = JWTSchemas(
        user_id=str(user.id),
        expire=datetime.now(timezone.utc) + timedelta(minutes=15)
    )

    #encode jwt token (we will call the encode function from jose)
    encoded_jwt = jwt.encode(jwt_data.dict(), SECRET_KEY, algorithm=ALGORITHM)
    return AuthResponse(
        user=user,
        token=encoded_jwt
    )
