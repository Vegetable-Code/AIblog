from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    PROJECT_NAME: str = "Blog API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    DATABASE_URL: str = "mysql+pymysql://root:password@localhost:3306/blog_db"
    # Support Railway MySQL plugin: auto-convert mysql:// to mysql+pymysql://
    MYSQL_URL: Optional[str] = None
    SECRET_KEY: str = "your-secret-key-change-in-production-abc123xyz"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
