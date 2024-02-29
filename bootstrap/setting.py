from functools import lru_cache

from pydantic import Field  # noqa: F401
from pydantic_settings import BaseSettings, SettingsConfigDict

from bootstrap.token import AccessTokenSettings, RefreshTokenSettings

from .base import base_model_config
from .db import SQLAlchmeySettings


class Settings(BaseSettings):
    access_token: AccessTokenSettings = AccessTokenSettings(
        _env_prefix="ACCESS_TOKEN__"
    )
    refresh_token: RefreshTokenSettings = RefreshTokenSettings(
        _env_prefix="REFRESH_TOKEN__"
    )
    db: SQLAlchmeySettings = SQLAlchmeySettings(_env_prefix="DB__")

    model_config: SettingsConfigDict = base_model_config


@lru_cache()
def get_settings():
    return Settings()
