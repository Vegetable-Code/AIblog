import re
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc
import markdown
from datetime import datetime, timezone
from pydantic import BaseModel
from ..core.database import get_db
from ..core.deps import get_current_user, get_current_active_superuser
from ..models.post import Post
from ..models.tag import Tag
from ..models.user import User
from ..schemas.post import PostCreate, PostUpdate

class BatchDeleteRequest(BaseModel):
    ids: list[int]

router = APIRouter(prefix="/posts", tags=["文章"])

def _post_to_detail(post):
    cat = post.category
    return {
        "id": post.id, "title": post.title, "slug": post.slug,
        "summary": post.summary or "", "content": post.content,
        "content_html": post.content_html or "", "cover_image": post.cover_image or "",
        "is_published": post.is_published, "is_top": post.is_top, "views_count": post.views_count,
        "category": {"id": cat.id, "name": cat.name, "slug": cat.slug, "description": cat.description or "", "created_at": cat.created_at, "post_count": 0} if cat else None,
        "tags": [{"id": t.id, "name": t.name, "slug": t.slug, "created_at": t.created_at, "post_count": 0} for t in post.tags],
        "created_at": post.created_at, "updated_at": post.updated_at, "published_at": post.published_at,
    }

def _md_to_html(content: str) -> str:
    return markdown.markdown(content, extensions=["fenced_code", "codehilite", "tables", "toc"])

@router.get("")
def list_posts(page: int = Query(1, ge=1), page_size: int = Query(10, ge=1, le=50),
               category_id: Optional[int] = None, tag_id: Optional[int] = None,
               keyword: Optional[str] = None, published_only: bool = Query(True), db: Session = Depends(get_db)):
    query = db.query(Post).options(joinedload(Post.category), joinedload(Post.tags), joinedload(Post.author))
    if published_only:
        query = query.filter(Post.is_published == True)
    if category_id:
        query = query.filter(Post.category_id == category_id)
    if tag_id:
        query = query.filter(Post.tags.any(Tag.id == tag_id))
    if keyword:
        query = query.filter(Post.title.contains(keyword) | Post.summary.contains(keyword))
    query = query.order_by(desc(Post.is_top), desc(Post.published_at), desc(Post.created_at))
    total = query.count()
    posts = query.offset((page - 1) * page_size).limit(page_size).all()
    return {"items": [_post_to_detail(p) for p in posts], "total": total, "page": page, "page_size": page_size, "total_pages": (total + page_size - 1) // page_size}


@router.get("/{slug}")
def get_post(slug: str, db: Session = Depends(get_db)):
    post = db.query(Post).options(joinedload(Post.category), joinedload(Post.tags), joinedload(Post.author)).filter(Post.slug == slug).first()
    if not post:
        raise HTTPException(status_code=404, detail="文章不存在")
    post.views_count += 1
    db.commit()
    return _post_to_detail(post)

@router.post("")
def create_post(data: PostCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_superuser)):
    slug = data.slug or re.sub(r'-+', '-', re.sub(r'[^a-z0-9\u4e00-\u9fa5]+', '-', data.title.lower())).strip('-')
    content_html = _md_to_html(data.content)
    post = Post(title=data.title, slug=slug, summary=data.summary or "", content=data.content,
                content_html=content_html, cover_image=data.cover_image or "", is_published=data.is_published,
                is_top=data.is_top or False, category_id=data.category_id, author_id=current_user.id,
                published_at=datetime.now(timezone.utc) if data.is_published else None)
    if data.tag_ids:
        tags = db.query(Tag).filter(Tag.id.in_(data.tag_ids)).all()
        post.tags = tags
    db.add(post)
    db.commit()
    db.refresh(post)
    return {"message": "创建成功", "id": post.id}

@router.put("/{post_id}")
def update_post(post_id: int, data: PostUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_superuser)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="文章不存在")
    update_data = data.model_dump(exclude_unset=True)
    if "slug" in update_data and not update_data["slug"]:
        update_data["slug"] = re.sub(r'-+', '-', re.sub(r'[^a-z0-9\u4e00-\u9fa5]+', '-', data.title.lower())).strip('-') if data.title else f"post-{post_id}"
    if "content" in update_data:
        update_data["content_html"] = _md_to_html(data.content)
    if "is_published" in update_data and data.is_published and not post.published_at:
        update_data["published_at"] = datetime.now(timezone.utc)
    if "tag_ids" in update_data:
        tags = db.query(Tag).filter(Tag.id.in_(data.tag_ids)).all() if data.tag_ids else []
        post.tags = tags
        del update_data["tag_ids"]
    for key, value in update_data.items():
        setattr(post, key, value)
    db.commit()
    return {"message": "更新成功"}

@router.delete("/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_superuser)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="文章不存在")
    db.delete(post)
    db.commit()
    return {"message": "删除成功"}

@router.post("/batch-delete")
def batch_delete_posts(data: BatchDeleteRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_superuser)):
    deleted = db.query(Post).filter(Post.id.in_(data.ids)).delete(synchronize_session=False)
    db.commit()
    return {"message": f"成功删除 {deleted} 篇文章", "deleted_count": deleted}

# Separate router for ID-based lookup (avoids conflict with /{slug})
detail_router = APIRouter(prefix="/posts", tags=["文章"])

@detail_router.get("/detail/{post_id}")
def get_post_by_id(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).options(joinedload(Post.category), joinedload(Post.tags), joinedload(Post.author)).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="文章不存在")
    return _post_to_detail(post)
