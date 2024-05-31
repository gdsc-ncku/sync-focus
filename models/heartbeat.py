from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Heartbeat(Base):
    __tablename__ = "heartbeats"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    # user_id: Mapped[str] = mapped_column(ForeignKey(User.id), unique=True)
    user_id: Mapped[str] = mapped_column(index=True)
    entity: Mapped[str] = mapped_column(index=True, nullable=True)
    type: Mapped[str] = mapped_column(index=True, nullable=True)
    category: Mapped[str] = mapped_column(index=True, nullable=True)
    browser: Mapped[str] = mapped_column(index=True)

    domain: Mapped[str] = mapped_column(index=True)  # page domain
    path: Mapped[str] = mapped_column(index=True)  # page path
    user_agent: Mapped[str] = mapped_column()  # user agent

    time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), index=True, nullable=True
    )
    hash: Mapped[str] = mapped_column(index=True, unique=True, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
