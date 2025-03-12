import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

    DB_HOST: str = os.getenv('DB_HOST', '')
    DB_PORT: int = int(os.getenv('DB_PORT', 5432))
    DB_USER: str = os.getenv('DB_USER', '')
    POSTGRES_PASSWORD: str = os.getenv('POSTGRES_PASSWORD', '')
    DB_NAME: str = os.getenv('DB_NAME', '')

    @property
    def DB_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.POSTGRES_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()
