from fastapi import APIRouter

from library.schemas.register import UserPublic
from library.schemas.users import UserUpdate

router = APIRouter(prefix="/user")

@router.put("/update", response_model=UserPublic)
async def register(data: UserUpdate):
    pass
