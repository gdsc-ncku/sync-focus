from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class Setting(BaseModel):
    user_id: Optional[UUID]
    raw: Optional[str]
    rev: Optional[int]

    model_config = ConfigDict(from_attributes=True)


class UpdateSettingRequest(BaseModel):
    rev: int
    raw: str

    model_config = ConfigDict(from_attributes=True)


class CreateSettingRequest(BaseModel):
    rev: int
    raw: str

    model_config = ConfigDict(from_attributes=True)
