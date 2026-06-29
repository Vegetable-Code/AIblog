"""
初始化脚本：创建初始管理员账号
用法: python init_user.py
请先修改数据库连接信息
"""
import os
import sys

# 添加项目根目录到 path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal, engine, Base
from app.core.security import get_password_hash
from app.models import User

# 创建所有表
Base.metadata.create_all(bind=engine)

def init():
    db = SessionLocal()
    try:
        # 检查是否已有管理员
        admin = db.query(User).filter(User.is_superuser == True).first()
        if admin:
            print(f"管理员已存在: {admin.username}")
            return

        # 创建默认管理员
        admin = User(
            username="admin",
            email="admin@blog.com",
            hashed_password=get_password_hash("admin123"),
            nickname="管理员",
            is_active=True,
            is_superuser=True,
        )
        db.add(admin)
        db.commit()
        print("初始化成功！")
        print("用户名: admin")
        print("密码: admin123")
    finally:
        db.close()

if __name__ == "__main__":
    init()
