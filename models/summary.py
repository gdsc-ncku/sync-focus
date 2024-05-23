from uuid import uuid4
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .user import User


class Summary(Base):
    __tablename__ = "summary"
    id: Mapped[str] = mapped_column(primary_key=True, index=True, default=uuid4().hex)
    user_id: Mapped[str] = mapped_column(ForeignKey(User.id), index=True)
    from_time: Mapped[datetime] = mapped_column(index=True)
    to_time: Mapped[datetime] = mapped_column(index=True)

