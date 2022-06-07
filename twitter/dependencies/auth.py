from jose import jwt, JWTError
from fastapi import Depends, HTTPException
from fastapi.security import (OAuth2PasswordBearer, SecurityScopes,)
from config import SECRET_KEY, ALGORITHM
from library.schemas.auth import JWTSchema
from pydantic import ValidationError

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login/",
    scopes={"base": "For ordinary users", "root": "For super users"},
    )

async def get_current_user(
    security_scopes: SecurityScopes, token: Str =Depends(oauth2_scheme)

):
    auth_execption = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        details= 'your auth token is invalid'
    )
    try:
        payload = jwt.decode(
            token, (SECRET_KEY), algorithms=[ALGORITHM]
            )
            user_id = payload.get('user_id')
            expire = payload.get('expire')

            if user_id is None or expire is None:
                raise auth_execption
    except (JWTError, ValidationError):
            raise auth_execption