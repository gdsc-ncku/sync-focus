from typing import TYPE_CHECKING

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .base import base_model_config

if TYPE_CHECKING:
    from .setting import Settings


# Create engine
def NewSessionMaker(settings: "Settings"):
    engine = create_engine(
        f"{settings.db.engine}://{settings.db.db_username}:{settings.db.db_password}@{settings.db.db_host}/{settings.db.db_name}",
    )
    return engine, sessionmaker(
        autocommit=settings.db.session_autocommit,
        autoflush=settings.db.session_autoflush,
        bind=engine,
    )


class SQLAlchmeySettings(BaseSettings):
    engine: str = Field(
        default="postgresql",
        alias="DATABASE_ENGINE",
    )
    db_name: str = Field(
        default="sync-focus-db",
        alias="DATABASE_NAME",
    )
    db_username: str = Field(
        default="postgres",
        alias="DATABASE_USERNAME",
    )
    db_password: str = Field(
        default="postgres",
        alias="DATABASE_PASSWORD",
    )
    db_host: str = Field(
        default="localhost",
        alias="DATABASE_HOST",
    )
    echo: bool = Field(
        default=False,
        alias="ECHO",
    )
    pool_size: int = Field(
        default=5,
        alias="POOL_SIZE",
    )
    max_overflow: int = Field(
        default=10,
        alias="MAX_OVERFLOW",
    )
    pool_timeout: int = Field(
        default=30,
        alias="POOL_TIMEOUT",
    )
    pool_recycle: int = Field(
        default=60,
        alias="POOL_RECYCLE",
    )
    track_modifications: bool = Field(
        default=False,
        alias="TRACK_MODIFICATIONS",
    )
    session_autocommit: bool = Field(
        default=False,
        alias="SESSION_AUTOCOMMIT",
    )
    session_autoflush: bool = Field(
        default=False,
        alias="SESSION_AUTOFLUSH",
    )

    model_config: SettingsConfigDict = base_model_config

    def get_sql_connection(self):
        return f"{self.engine}://{self.db_username}:{self.db_password}@{self.db_host}/{self.db_name}"
