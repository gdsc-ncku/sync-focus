from typing import Optional
from datetime import datetime

from pydantic import BaseModel, ConfigDict

class SummaryItem(BaseModel):
    id: Optional[str]
    summary_id: Optional[str]
    type: Optional[int]
    total: Optional[int]
    key: Optional[str]
    
    model_config = ConfigDict(from_attributes=True)

