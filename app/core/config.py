from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROFILE: str = "local"
    API_PREFIX: str = "/api/v1"
    ROOT_PATH: str = str(Path(__file__).parent.parent.parent)

    HF_TOKEN: str
    LANGSMITH_API_KEY: str

    GOOGLE_API_KEY: str
    GEMINI_MODEL: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()
