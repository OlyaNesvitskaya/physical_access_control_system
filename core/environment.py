from typing import Final
from pydantic import EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
import os

os.environ.setdefault('APP_CONFIG_FILE', 'local')


class Settings(BaseSettings):
    API_VERSION: str = '1.0.0'
    APP_NAME: str = 'PhysicalAccessControlSystem'
    DATABASE_URL: str
    DEBUG_MODE: bool
    TOKEN_KEY: str = ""
    AUTH_URL: Final = "token"
    TOKEN_TYPE: Final = "bearer"
    TOKEN_EXPIRE_MINUTES: Final = 60 * 24
    TOKEN_ALGORITHM: Final = "HS256"
    FIRST_SUPERUSER: EmailStr = "example@example.com"
    FIRST_SUPERUSER_PASSWORD: str = "12345"

    model_config = SettingsConfigDict(
            env_file=Path(__file__).parent.parent / f"{os.getenv('APP_CONFIG_FILE', '')}.env",
            case_sensitive=True)


settings = Settings()
