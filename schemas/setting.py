from typing import Optional

from pydantic import BaseModel, ConfigDict

class Setting(BaseModel):
    user_id: Optional[str]
    raw: Optional[str]
    rev: Optional[str]

    model_config = ConfigDict(from_attributes=True)

class UpdateSettingRequest:
    rev: int
    raw: str

class CreateSettingRequest:
    rev: int
    raw: str

