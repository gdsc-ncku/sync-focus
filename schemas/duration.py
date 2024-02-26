from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel, Field

from .heartbeat import Heartbeat


class Duration(BaseModel):
    user_id: Optional[str] = None
    time: Optional[datetime] = None
    duration: Optional[timedelta] = None
    domain: Optional[str] = None
    browser: Optional[str] = None
    entity: Optional[str] = None
    heartbeat_num: Optional[int] = Field(
        default=None,
        exclude=True,
    )

    @classmethod
    def from_heartbeat(cls, heartbeat: Heartbeat) -> "Duration":
        return cls(
            user_id=heartbeat.user_id,
            time=heartbeat.time,
            duration=timedelta(seconds=0),
            domain=heartbeat.domain,
            browser=heartbeat.browser,
            entity=heartbeat.entity,
            heartbeat_num=1,
        )
