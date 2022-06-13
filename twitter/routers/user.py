from fastapi import APIRouter, Security
from models.users import User

from library.schemas.register import UserPublic
from library.schemas.users import UserUpdate
from library.dependencies.auth import get_current_user

router = APIRouter(prefix="/user")

@router.put("/update/", response_model=UserPublic)
async def update(
    current_user= Security(get_current_user, scopes=["base","roots"]),
    ):
       await User.get(id=current_user.id).update(**data.dict(exclude=True))

       return User.get(id=current_user.id)



@router.delete("/delete/", response_model=UserPublic)
async def delete(
    current_user= Security(get_current_user, scopes=["base","roots"]),
    ):
  await User.get(id=current_user.id).delete()