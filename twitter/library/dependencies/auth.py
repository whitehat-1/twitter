from jose import JWTError, jwt
from fastapi import Depends, HTTPException,status
from fastapi.security import (OAuth2PasswordBearer, SecurityScopes,)
from config import SECRET_KEY, ALGORITHM
from library.schemas.auth import JWTSchema 
from pydantic import BaseModel, ValidationError
from datetime import datetime, timedelta, timezone

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login/",
    scopes={"base": "For ordinary users", "root": "For super users"},
    )

async def get_current_user(
    security_scopes: SecurityScopes, token: str =Depends(oauth2_scheme)

):
    auth_exeception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        details= 'your auth token is invalid Or Try logging in again',
    )
    try:
        payload = jwt.decode(
            token, (SECRET_KEY), algorithms=[ALGORITHM]
            )
        user_id = payload.get('user_id')
        expire = payload.get('expire')

        token_data = JWTSchema(
            user_id = user_id,
            expire = expire
        )

        if user_id is None or expire is None:
                raise auth_exeception
    except (JWTError, ValidationError):
            raise auth_exeception

    #check if the token is expired
    if datetime.now(timezone.utc) > token_data.expire:
        raise auth_exeception
        
    
    user = await user.get_or_none(id=token_data.user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user