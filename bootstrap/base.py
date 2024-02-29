from pydantic_settings import SettingsConfigDict

base_model_config: SettingsConfigDict = SettingsConfigDict(
    env_file=(
        "example.env",
        ".env",
    ),
    env_file_encoding="utf-8",
    extra="ignore",
    case_sensitive=True,
    env_nested_delimiter="__",
)
