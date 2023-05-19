from typing import Literal

from pydantic import BaseSettings


class Settings(BaseSettings):
    API_PORT: int = "80"
    ENV_TYPE: Literal['local', 'staging', 'production'] = "local"
    API_KEY: str = ""

    MONGODB_HOST: str = ""
    MONGODB_PORT: int = 27017
    MONGODB_USERNAME: str = ""
    MONGODB_PASSWORD: str = ""
    MONGODB_DATABASE: str = ""

    OPEN_AI_API_KEY: str = ""

    class Config:
        case_sensitive = True


settings = Settings()
