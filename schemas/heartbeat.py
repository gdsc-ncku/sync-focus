from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class DomainStat(BaseModel):
    user_id: Optional[str] = None
    domain: Optional[str] = None
    first_time: Optional[datetime] = None
    last_time: Optional[datetime] = None
    count: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class Heartbeat(BaseModel):
    id: Optional[UUID] = None
    user_id: Optional[str] = None
    entity: Optional[str] = None
    type: Optional[str] = None
    category: Optional[str] = None
    browser: Optional[str] = None
    domain: Optional[str] = None
    path: Optional[str] = None
    user_agent: Optional[str] = None
    time: Optional[datetime] = None
    hash: Optional[str] = None
    created_at: Optional[datetime] = None

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
    entity: Optional[str] = None
    type: Optional[str] = None
    category: Optional[str] = None
    browser: Optional[str] = None
    domain: Optional[str] = None
    path: Optional[str] = None
    user_agent: Optional[str] = None
    time: Optional[datetime] = None
