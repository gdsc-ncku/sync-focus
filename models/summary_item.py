from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .user import User

class SummaryItem(Base):
    __tablename__ = "summary_item"
    id: Mapped[str] = mapped_column(primary_key=True, index=True, default=uuid4().hex)
    summary_id: Mapped[str] = mapped_column(ForeignKey("summary.id"), index=True)
    type: Mapped[int] = mapped_column(index=True)
    total: Mapped[int] = mapped_column(index=True)
    key: Mapped[str] = mapped_column(index=True)