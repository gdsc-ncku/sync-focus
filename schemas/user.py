from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class User(BaseModel):
    username: Optional[str]
    api_key: Optional[str]
    is_admin: Optional[bool]
    created_at: Optional[datetime]
    last_login: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)


class CreateUserRequest(BaseModel):
    username: Optional[str]
    password: str

    model_config = ConfigDict(from_attributes=True)


class Birthday(BaseModel):
    birthday: date


class TimeByUser(BaseModel):
    user: str
    time: datetime
