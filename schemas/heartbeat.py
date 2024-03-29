from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class DomainStat(BaseModel):
    user_id: Optional[str]
    domain: Optional[str]
    first_time: Optional[datetime]
    last_time: Optional[datetime]
    count: Optional[int]

    model_config = ConfigDict(from_attributes=True)


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

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_request(cls, request: "HeartbeatCreateRequest") -> "Heartbeat":
        return cls(
            entity=request.entity,
            type=request.type,
            category=request.category,
            browser=request.browser,
            domain=request.domain,
            path=request.path,
            user_agent=request.user_agent,
            time=request.time,
        )


class HeartbeatCreateRequest(BaseModel):
    entity: Optional[str]
    type: Optional[str]
    category: Optional[str]
    browser: Optional[str]
    domain: Optional[str]
    path: Optional[str]
    user_agent: Optional[str]
    time: Optional[datetime]
