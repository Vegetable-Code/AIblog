import os
import sys

# Add parent to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal, engine, Base
from app.models.user import User
from app.core.security import get_password_hash
from sqlalchemy import text

def init():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Check if admin exists
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            print("Creating admin user...")
            admin = User(
                username="admin",
                email="admin@blog.com",
                hashed_password=get_password_hash("admin123"),
                nickname="管理员",
                is_superuser=True,
                is_active=True,
            )
            db.add(admin)
            db.commit()
            print("Admin user created: admin / admin123")
        else:
            print("Admin user already exists")
    finally:
        db.close()
    
    print("Database initialization complete!")

if __name__ == "__main__":
    init()
