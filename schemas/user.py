from datetime import date, datetime

from pydantic import BaseModel

# User Schema


class Base(BaseModel):
    username: str
    birthday: date


class Register(Base):
    password: str


class Password(BaseModel):
    password: str


class Birthday(BaseModel):
    birthday: date


class TimeByUser(Base):
    user: str
    time: datetime
