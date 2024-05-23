from fastapi import APIRouter, Depends, HTTPException, Response, status

# from service.utils import create_access_token, create_refresh_token
from api.services import get_user_service
from schemas.token import Token
from schemas.user import UserLoginRequest
from service.user import UserService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=Token)
def login(
    response: Response,
    form_data: UserLoginRequest,
    user_service: UserService = Depends(get_user_service),
):
    user = user_service.get_user_by_username(username=form_data.username)
    if not user or user.password != form_data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = user_service.create_access_token(data={"user_id": str(user.id)})
    refresh_token = user_service.create_refresh_token(data={"user_id": str(user.id)})

    response.set_cookie(
        "access_token",
        access_token,
        httponly=True,
        samesite="strict",
        secure=False,
    )

    response.set_cookie(
        "refresh_token",
        refresh_token,
        httponly=True,
        samesite="strict",
        secure=False,
    )

    return Token(
        access_token=access_token,
        token_type="Bearer",
    )


# @router.post("/refresh", response_model=Token)
# async def refresh(
#     request: Request,
#     response: Response,
#     user_service: UserService = Depends(get_user_service),
# ):
#     credentials_exception = HTTPException(
#         status_code=401,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         refresh_token = request.cookies.get("refresh_token")
#         if not refresh_token:
#             raise credentials_exception

#         payload = jwt.decode(
#             refresh_token,
#             settings.refresh_token_secret,
#             algorithms=["HS256"],
#         )

#         username: str = payload.get("username")
#         if username is None:
#             raise credentials_exception

#     except Exception as e:
#         credentials_exception.detail = str(e)
#         raise credentials_exception

#     access_token = await create_access_token(data={"username": username})
#     refresh_token = await create_refresh_token(data={"username": username})

#     user_service.update_user_login(username)
#     expired_time = (
#         int(datetime.now(tz=timezone.utc).timestamp() * 1000)
#         + timedelta(minutes=settings.access_token_expire_minutes).seconds * 1000
#     )

#     response.set_cookie(
#         "refresh_token",
#         refresh_token,
#         httponly=True,
#         samesite="strict",
#         secure=False,
#         expires=timedelta(settings.refresh_token_expire_minutes),
#     )

#     return Token(
#         access_token=access_token,
#         expires_in=expired_time,
#         token_type="Bearer",
#     )


# @router.post("/logout")
# async def logout(response: Response):
#     response.delete_cookie("refresh_token")
#     return {"message": "Logout successfully"}
