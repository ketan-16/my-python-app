import os
from dataclasses import dataclass

_TRUTHY = {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    app_name: str
    debug: bool


def load_settings() -> Settings:
    """Read settings from environment variables, falling back to defaults."""
    return Settings(
        app_name=os.getenv("APP_NAME", "My Python App"),
        debug=os.getenv("APP_DEBUG", "false").strip().lower() in _TRUTHY,
    )
