from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status

from schemas.user import CreateUserRequest, User
from service.user import UserService

# from auth.action import get_current_user
from .services import get_user_service

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=List[User])
def get_users(user_service: UserService = Depends(get_user_service)):
    return user_service.get_users()


@router.post("")
def register(
    new_user: CreateUserRequest, user_service: UserService = Depends(get_user_service)
):
    db_user = user_service.get_user_by_username(username=new_user.username)
    if db_user:
        raise HTTPException(status_code=409, detail="Username already registered")
    user_service.create_user(new_user)
    return status.HTTP_201_CREATED


@router.delete("", deprecated=True)
def delete_user(
    # current_user: user_schema.Base = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
    username: str = Query(...),
):
    user_service.delete_user(username=username)
    # return await db.delete_user(username=current_user.username)
    return "ok"


# @router.put("/password", deprecated=True)
# async def update_password(
#     request: user_schema.Password,
#     current_user: user_schema.Base = Depends(get_current_user),
#     db: UserService = Depends(get_user_crud),
# ):
#     # return await db.update_password(  username=current_user.username , password=request.password )
#     return "deprecated"


# @router.put("/birthday", deprecated=True)
# async def update_birthday(
#     request: user_schema.Birthday,
#     current_user: user_schema.Base = Depends(get_current_user),
#     db: UserService = Depends(get_user_crud),
# ):
#     # return await db.update_birthday( username=current_user.username ,birthday=request.birthday )
#     return "deprecated"


# @router.get("/me", response_model=user_schema.Base, deprecated=True)
# async def protected(current_user: user_schema.Base = Depends(get_current_user)):
#     # return current_user
#     return "deprecated"
