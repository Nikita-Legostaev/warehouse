from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import ConfigDict

class Settings(BaseSettings):
    model_config =  SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    POSTGRES_PASSWORD: str
    DB_NAME: str
    
    @property
    def DB_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.POSTGRES_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
settings = Settings()
