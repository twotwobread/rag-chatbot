from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    GOOGLE_API_KEY: str
    GEMINI_MODEL: str

    DB_MODE: str = "sqlite"
    DB_HOST: str = "database.db"
    DB_PORT: int = -1
    DB_SCHEMA: str = ""
    DB_USER: str = ""
    DB_PASSWORD: str = ""
    DB_SCHEME: str = "sqlite+aiosqlite"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()
