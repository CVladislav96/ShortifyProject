from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"
    api_title: str = "Shortify API"
    api_description: str = "URL Shortener Service"
    api_version: str = "1.0.0"
    cors_origins: List[str] = ["*"]
    rate_limit_calls: int = 10
    rate_limit_period: int = 60
    slug_length: int = 6
    environment: str = "development"
    
    class Config:
        env_file = ".env"


settings = Settings()
