from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    GOOGLE_API_KEY: str
    GEMINI_MODEL: str

    DB_HOST: str
    DB_PORT: int
    DB_SCHEMA: str
    DB_USER: str
    DB_PASSWORD: str
    DB_SCHEME: str = "postgresql+asyncpg"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()
