from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import APIKeyCookie
from jose import jwt

# from service.utils import create_access_token, create_refresh_token
from bootstrap.setting import setting

router = APIRouter(prefix="/auth", tags=["auth"])


cookie_schema = APIKeyCookie(name="access_token")


def required_login(token: Annotated[str, Depends(cookie_schema)]) -> str:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    payload = jwt.decode(token, setting.access_token.secret, algorithms=["HS256"])

    if (payload is None) or ("user_id" not in payload):
        raise credentials_exception
    return payload.get("user_id")
