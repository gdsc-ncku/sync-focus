from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class Summary(BaseModel):
    id: Optional[str]
    user_id: Optional[str]
    from_time: Optional[datetime]
    to_time: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)


class ListDomainRequest(BaseModel):
    offset: int
    limit: int


class ListPathRequest(BaseModel):
    domain: str


class ListAgentRequest(BaseModel):
    domain: str
