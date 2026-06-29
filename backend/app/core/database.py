from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import settings


def get_database_url() -> str:
    """Get database URL, supporting Railway MySQL plugin format."""
    if settings.MYSQL_URL:
        # Railway provides mysql://user:pass@host:port/db
        # Convert to mysql+pymysql://user:pass@host:port/db
        return settings.MYSQL_URL.replace("mysql://", "mysql+pymysql://", 1)
    return settings.DATABASE_URL


engine = create_engine(get_database_url(), pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
