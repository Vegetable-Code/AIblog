from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..core.deps import get_current_active_superuser
from ..models.comment import Comment
from ..models.post import Post
from ..models.user import User
from ..core.deps import get_current_user_optional
from ..schemas.comment import CommentCreate, CommentUpdate

router = APIRouter(prefix="/comments", tags=["\u8bc4\u8bba"])

def _build_tree(comments):
    result, reply_map = [], {}
    for c in comments:
        cd = {"id": c.id, "content": c.content, "nickname": c.nickname, "email": c.email or "",
              "website": c.website or "", "is_approved": c.is_approved, "post_id": c.post_id,
              "parent_id": c.parent_id, "created_at": c.created_at, "replies": []}
        reply_map.setdefault(c.parent_id or 0, []).append(cd)
        if not c.parent_id:
            result.append(cd)
    for p in result:
        p["replies"] = reply_map.get(p["id"], [])
    return result

@router.get("/post/{post_id}")
def get_post_comments(post_id: int, db: Session = Depends(get_db)):
    comments = db.query(Comment).filter(Comment.post_id == post_id, Comment.is_approved == True).order_by(Comment.created_at.asc()).all()
    return _build_tree(comments)

@router.get("")
def list_all_comments(page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100),
                      db: Session = Depends(get_db), user=Depends(get_current_active_superuser)):
    query = db.query(Comment).order_by(Comment.created_at.desc())
    total = query.count()
    comments = query.offset((page - 1) * page_size).limit(page_size).all()
    return {"items": [{"id": c.id, "content": c.content, "nickname": c.nickname, "email": c.email or "",
            "website": c.website or "", "is_approved": c.is_approved, "post_id": c.post_id,
            "parent_id": c.parent_id, "created_at": c.created_at} for c in comments],
            "total": total, "page": page, "page_size": page_size, "total_pages": (total + page_size - 1) // page_size}

@router.post("")
def create_comment(data: CommentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user_optional)):
    post = db.query(Post).filter(Post.id == data.post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="文章不存在")
    if data.parent_id:
        if not db.query(Comment).filter(Comment.id == data.parent_id).first():
            raise HTTPException(status_code=404, detail="父评论不存在")

    nickname = data.nickname or current_user.nickname or current_user.username if current_user else (data.nickname or "匿名")
    email = (data.email or current_user.email) if current_user else (data.email or "")

    comment = Comment(
        content=data.content,
        nickname=nickname,
        email=email,
        website=data.website or "",
        post_id=data.post_id,
        parent_id=data.parent_id,
        user_id=current_user.id if current_user else None,
        is_approved=False,
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return {"message": "评论成功，等待审核"}

@router.put("/{comment_id}")
def update_comment(comment_id: int, data: CommentUpdate, db: Session = Depends(get_db), user=Depends(get_current_active_superuser)):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="\u8bc4\u8bba\u4e0d\u5b58\u5728")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(comment, key, value)
    db.commit()
    return {"message": "\u66f4\u65b0\u6210\u529f"}

@router.delete("/{comment_id}")
def delete_comment(comment_id: int, db: Session = Depends(get_db), user=Depends(get_current_active_superuser)):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="\u8bc4\u8bba\u4e0d\u5b58\u5728")
    db.delete(comment)
    db.commit()
    return {"message": "\u5220\u9664\u6210\u529f"}
