from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

TYPE_ENVIRONMENT = Literal["local", "test", "staging", "production"]


class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(env_nested_delimiter="__")

    APP_NAME: str = "bootstrap"
    DEBUG: bool = False
    ENVIRONMENT: TYPE_ENVIRONMENT = "local"
