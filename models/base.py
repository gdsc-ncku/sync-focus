import datetime
from uuid import uuid4

from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


def generate_id():
    return uuid4().hex


class Base(DeclarativeBase):
    # is_deleted: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime.datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(
        default=func.now(), onupdate=func.now()
    )
