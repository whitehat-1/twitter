from fastapi import FastAPI

from library.database.database import create_start_app_handler
from routers.auth import router as AuthRouter
from routers.content import router as ContentRouter
from schemas import JWTSchema
from jose import jwt, JWTError
from pydantic import ValidationError
from config import SECRET_KEY, ALGORITHM

def get_application():

    # start the application.
    app = FastAPI()

    # Connect to database.
    app.add_event_handler("startup", create_start_app_handler(app))
    app.include_router(AuthRouter)
    app.include_router(ContentRouter)

    return app


app = get_application()


@app.get("/")
async def home():
    return {"detail": "hello world!"}


class Hasher():
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)


@app.post("/register/")
async def register(data: Registration):
    """User Registration endpoint"""
    hashed_password = pwd_context.hash(data.password)
    user_create = await Register.create(
        **data.dict(exclude_unset=True),
    )
        # Generate an auth token.
    jwt_data = JWTSchema(user_id=str(user_create.id))
    to_encode = jwt_data.dict()
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    to_encode.update({"expire": str(expire)})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    context = {
        "user": data.full_name,
        "token": encoded_jwt
    }
    return context
 
@app.post("/auth/login/")
async def get_current_user(token: str):
    auth_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Your auth token is invalid.",
    )
    try:
        payload = jwt.decode(token, str(SECRET_KEY), algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        expire = payload.get("expire")

        token_data = JWTSchema(user_id=user_id, expire=expire)

        if user_id is None or expire is None:
            raise auth_exception
    except (JWTError, ValidationError):
        raise auth_exception  
    user = await Register.get_or_none(id=token_data.user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="This user does not exist.",
        )

    return user
