from pydantic import BaseModel
from starlette.exceptions import HTTPException


class BaseAPIException(HTTPException):
    def __init__(
        self,
        status_code: int,
        message: str,
        detail: str = None,
        error_code: str = None,
        **kwargs,
    ):
        super().__init__(status_code=status_code, detail=detail)
        self.message = message
        self.error_code = error_code


class ServiceException(HTTPException):
    def __init__(
        self,
        status_code: int,
        message: str,
        detail: str = None,
        error_code: str = None,
        **kwargs,
    ):
        super().__init__(status_code=status_code, detail=detail)
        self.message = message
        self.error_code = error_code


class HTTPError(BaseModel):
    detail: str

    class Config:
        json_schema_extra = {
            "example": {"detail": "HTTPException raised."},
        }
