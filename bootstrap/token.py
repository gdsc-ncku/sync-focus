from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from .base import base_model_config


class AccessTokenSettings(BaseSettings):
    secret: str = Field(
        default="123",
        alias="SECRET",
    )
    algorithm: str = Field(
        alias="ALGORITHM",
        default="HS256",
    )
    expire_minutes: int = Field(
        alias="EXPIRE_MINUTES",
        default=60,
    )

    model_config: SettingsConfigDict = base_model_config


class RefreshTokenSettings(BaseSettings):
    secret: str = Field(
        alias="SECRET",
        default="123",
    )
    algorithm: str = Field(
        alias="ALGORITHM",
        default="HS256",
    )
    expire_minutes: int = Field(
        alias="EXPIRE_MINUTES",
        default=60 * 24 * 7 * 4,
    )

    model_config: SettingsConfigDict = base_model_config
