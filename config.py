from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Bot Configuration
    BOT_TOKEN: str
    BOT_USERNAME: str
    SUPER_ADMIN_IDS: list[int]

    # Database
    DATABASE_URL: str
    # Fix Railway.io postgres:// -> postgresql+asyncpg://
    @property
    def ASYNC_DATABASE_URL(self) -> str:
        """Convert DATABASE_URL to async PostgreSQL URL if needed."""
        url = self.DATABASE_URL
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql+asyncpg://", 1)
        return url

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Userbot (Pyrogram) - Optional
    API_ID: Optional[int] = None
    API_HASH: Optional[str] = None
    USERBOT_SESSION_STRING: Optional[str] = None

    # Telegram Channels/Groups
    BASE_CHANNEL_ID: int
    LOG_CHANNEL_ID: int
    COMMENT_GROUP_ID: int

    # Broadcast Settings
    BROADCAST_BOT_RATE: int = 28  # requests per second
    BROADCAST_USERBOT_RATE: int = 20  # requests per second
    ALLOW_PAID_BROADCAST: bool = False

    # Logging & Other
    LOG_LEVEL: str = "INFO"
    TZ: str = "Asia/Tashkent"

    # Feature Flags
    FORCE_SUBSCRIPTION: bool = True
    MAINTENANCE_MODE: bool = False

    class Config:
        env_file = ".env"
        case_sensitive = True

    def has_userbot(self) -> bool:
        """Check if userbot credentials are configured."""
        return bool(
            self.API_ID
            and self.API_HASH
            and self.USERBOT_SESSION_STRING
        )

    def parse_super_admin_ids(self, value: str | list[int]) -> list[int]:
        """Parse comma-separated admin IDs."""
        if isinstance(value, list):
            return value
        if isinstance(value, str):
            return [int(x.strip()) for x in value.split(",")]
        return []

    @classmethod
    def settings_customise_sources(cls, settings_cls, init_settings, env_settings, dotenv_settings, file_settings):
        # Override SUPER_ADMIN_IDS parsing
        if "SUPER_ADMIN_IDS" in env_settings and isinstance(env_settings["SUPER_ADMIN_IDS"], str):
            env_settings["SUPER_ADMIN_IDS"] = [
                int(x.strip()) for x in env_settings["SUPER_ADMIN_IDS"].split(",")
            ]
        return init_settings, env_settings, dotenv_settings, file_settings


# Global settings instance
settings = Settings()
