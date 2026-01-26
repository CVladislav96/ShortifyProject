from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:6432/postgres"
    
    class Config:
        env_file = ".env"


settings = Settings()
