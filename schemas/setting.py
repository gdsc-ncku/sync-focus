from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

class Heartbeat(BaseModel):
    user_id: Optional[str]
    raw: Optional[str]
    rev: Optional[str]

    model_config = ConfigDict(from_attributes=True)
