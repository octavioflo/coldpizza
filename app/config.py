import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_engine: str
    
    model_config = SettingsConfigDict(env_file=f".env.{os.getenv('ENVIRONMENT', 'development')}")

settings = Settings()