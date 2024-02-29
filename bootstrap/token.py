from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from .base import base_model_config


class AccessTokenSettings(BaseSettings):
    SECRET: str = Field(
        default="123",
        alias="SECRET",
    )
    ALGORITHM: str = Field(
        default="HS256",
    )
    EXPIRE_MINUTES: int = Field(
        default=60,
    )

    model_config: SettingsConfigDict = base_model_config


class RefreshTokenSettings(BaseSettings):
    SECRET: str = Field(
        default="123",
    )
    ALGORITHM: str = Field(
        default="HS256",
    )
    EXPIRE_MINUTES: int = Field(
        default=60 * 24 * 7 * 4,
    )

    model_config: SettingsConfigDict = base_model_config
