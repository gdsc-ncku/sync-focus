import hashlib
import json
from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

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

    group_hash: Optional[str] = Field(
        default=None,
        exclude=True,
        title="Group Hash",
        description="A hash of the object to group by",
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

    def hashed(self):
        obj_dict = self.__dict__.copy()
        obj_dict.pop("heartbeat_num", None)
        obj_dict.pop("group_hash", None)
        obj_json = json.dumps(obj_dict, default=str)

        hash_obj = hashlib.sha256(obj_json.encode())
        self.group_hash = hash_obj.hexdigest()
        return self
