from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

if TYPE_CHECKING:
    from .user import User


class Setting(Base):
    __tablename__ = "setting"
    user_id: Mapped[str] = mapped_column(ForeignKey(User.id), index=True)
    raw: Mapped[str] = mapped_column(unique=True, default="{}")
    rev: Mapped[int] = mapped_column(DateTime(timezone=True), server_default=func.now())
