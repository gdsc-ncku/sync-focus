from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .user import User


class Setting(Base):
    __tablename__ = "settings"
    id: Mapped[UUID] = mapped_column(primary_key=True, index=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey(User.id), index=True)
    raw: Mapped[str] = mapped_column(unique=True, default="{}")
    rev: Mapped[int] = mapped_column(Integer, default=1)
