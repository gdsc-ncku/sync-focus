from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class DomainStat(BaseModel):
    user_id: Optional[str]
    domain: Optional[str]
    first_time: Optional[datetime]
    last_time: Optional[datetime]
    count: Optional[int]
