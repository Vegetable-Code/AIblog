import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal, engine, Base
from app.models.user import User
from app.core.security import get_password_hash


def init():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    
    # Ensure upload directory exists
    upload_root = os.environ.get("UPLOAD_ROOT", "/app/uploads")
    os.makedirs(upload_root, exist_ok=True)
    print(f"Upload directory ready: {upload_root}")
    
    db = SessionLocal()
    try:
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
    except Exception as e:
        print(f"Warning: Could not create admin user: {e}")
    finally:
        db.close()
    
    print("Database initialization complete!")

if __name__ == "__main__":
    init()
