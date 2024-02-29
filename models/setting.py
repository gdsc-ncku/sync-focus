from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from database.config import Base

# Create Setting class
class Setting(Base):
    __tablename__ = "setting"
    user_id: Mapped[str] = mapped_column(ForeignKey(User.id),index=True)
    raw: Mapped[str] = mapped_column(unique=True, default="{}")
    rev: Mapped[int] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
