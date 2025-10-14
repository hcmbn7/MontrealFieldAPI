from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List


class Settings(BaseSettings):
    DATABASE_URL: str
    API_PREFIX: str = "/api"
    PROJECT_NAME: str = "FieldFinder"
    DEBUG: bool = True
    ALLOWED_ORIGINS: List[str] = []

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
