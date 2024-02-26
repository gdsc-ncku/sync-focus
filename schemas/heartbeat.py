from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class DomainStat(BaseModel):
    user_id: Optional[str]
    domain: Optional[str]
    first_time: Optional[datetime]
    last_time: Optional[datetime]
    count: Optional[int]


class Heartbeat(BaseModel):
    id: Optional[str]
    user_id: Optional[str]
    entity: Optional[str]
    type: Optional[str]
    category: Optional[str]
    browser: Optional[str]
    domain: Optional[str]
    path: Optional[str]
    user_agent: Optional[str]
    time: Optional[datetime]
    hash: Optional[str]
    created_at: Optional[datetime]
