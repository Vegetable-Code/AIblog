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

    # SMTP settings for email verification
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_FROM_EMAIL: Optional[str] = None
    SMTP_USE_SSL: bool = False
    SENDGRID_API_KEY: Optional[str] = None
    RESEND_API_KEY: Optional[str] = None
    BREVO_API_KEY: Optional[str] = None

    # S3-compatible object storage (Cloudflare R2 / AWS S3 / MinIO)
    S3_ENDPOINT: Optional[str] = None
    S3_ACCESS_KEY_ID: Optional[str] = None
    S3_SECRET_ACCESS_KEY: Optional[str] = None
    S3_BUCKET_NAME: Optional[str] = None
    S3_PUBLIC_URL: Optional[str] = None
    S3_REGION: str = "auto"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
