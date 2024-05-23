from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import APIKeyCookie
from jose import ExpiredSignatureError, jwt

# from service.utils import create_access_token, create_refresh_token
from bootstrap.setting import setting

router = APIRouter(prefix="/auth", tags=["auth"])


cookie_schema = APIKeyCookie(name="access_token", auto_error=False)


def required_login(token: Annotated[str, Depends(cookie_schema)]) -> str:
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token, setting.access_token.secret, algorithms=["HS256"])
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Login expired, please login again",
        )

    if (payload is None) or ("user_id" not in payload):
        raise credentials_exception
    return payload.get("user_id")
