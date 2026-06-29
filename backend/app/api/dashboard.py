from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..core.database import get_db
from ..core.deps import get_current_active_superuser
from ..models.post import Post
from ..models.comment import Comment
from ..models.category import Category
from ..models.user import User

router = APIRouter(prefix="/dashboard", tags=["\u4eea\u8868\u76d8"])

@router.get("/stats")
def get_stats(db: Session = Depends(get_db), user=Depends(get_current_active_superuser)):
    return {
        "post_count": db.query(func.count(Post.id)).scalar(),
        "published_count": db.query(func.count(Post.id)).filter(Post.is_published == True).scalar(),
        "comment_count": db.query(func.count(Comment.id)).scalar(),
        "pending_comment_count": db.query(func.count(Comment.id)).filter(Comment.is_approved == False).scalar(),
        "category_count": db.query(func.count(Category.id)).scalar(),
        "user_count": db.query(func.count(User.id)).scalar(),
        "view_count": db.query(func.coalesce(func.sum(Post.views_count), 0)).scalar(),
    }

@router.get("/recent_posts")
def get_recent_posts(limit: int = 5, db: Session = Depends(get_db), user=Depends(get_current_active_superuser)):
    posts = db.query(Post).order_by(Post.created_at.desc()).limit(limit).all()
    return [{"id": p.id, "title": p.title, "is_published": p.is_published, "views_count": p.views_count, "created_at": p.created_at} for p in posts]
