from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    APP_NAME: str
    DATABASE_URL: str
    API_V1_PREFIX: str
    OPENAI_API_KEY: str

    model_config = SettingsConfigDict(
        env_file=".env", extra="allow", case_sensitive=True
    )


# caching env variables
@lru_cache()
def get_settings():
    return Settings()


# instantiating only once and reusing
settings = get_settings()
