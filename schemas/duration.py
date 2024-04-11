import hashlib
import json
from datetime import datetime, timedelta
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field

from .heartbeat import Heartbeat


class Duration(BaseModel):
    user_id: Optional[str] = None
    time: Optional[datetime] = None
    duration: Optional[timedelta] = None
    domain: Optional[str] = None
    browser: Optional[str] = None
    entity: Optional[str] = None  # Summary Type, domain, path, etc.
    heartbeat_num: Optional[int] = Field(
        default=None,
        exclude=True,
    )

    group_hash: Optional[str] = Field(
        default=None,
        exclude=True,
        title="Group Hash",
        description="A hash of the object to group by",
    )

    exclude_entity: Optional[bool] = Field(
        default=False,
        title="Exclude Entity",
        description="Whether to exclude the entity from the hash",
    )

    model_config = ConfigDict(from_attributes=True)

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

    def hash_include(self, field: str, v: Any):
        if field == "entity":
            return not self.exclude_entity
        if (
            field in ["time", "duration", "heartbeat_num", "group_hash"]
            or field[0].islower()
        ):
            return False
        return True

    def hashed(self):
        try:
            filtered_dict = {
                k: v for k, v in self.__dict__.items() if self.hash_include(k, v)
            }
            serialized = json.dumps(filtered_dict, sort_keys=True).encode()
            self.group_hash = hashlib.sha256(serialized).hexdigest()
        except Exception as e:
            print(f"CRITICAL ERROR: failed to hash object - {e}")
        return self
