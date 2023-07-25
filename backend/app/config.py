from datetime import datetime

from pydantic import Field
from pydantic_settings import BaseSettings
from pydantic_settings.sources import PydanticBaseSettingsSource
from pytz import timezone


class Settings(BaseSettings):
    version: str = "invalid"
    backend_env: str = Field("local", pattern=r"^(local|ci|dev|stage|prod)$")
    start_at: str = Field(
        default_factory=lambda: datetime.now(tz=timezone("Asia/Seoul")).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    )
    timezone: str = "Asia/Seoul"
    slack_webhook_url: str = "invalid"
    db_url: str = "invalid"

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,  # /run/secrets
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            env_settings,  # os.environ
            dotenv_settings,  # .env
            init_settings,  # init
        )

    class Config:
        env_file = ".env.local"
        env_file_encoding = "utf-8"


settings = Settings()
