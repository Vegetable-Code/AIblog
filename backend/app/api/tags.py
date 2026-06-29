from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..core.database import get_db
from ..core.deps import get_current_active_superuser
from ..models.tag import Tag
from ..models.post_tag import post_tags
from ..schemas.tag import TagCreate, TagUpdate, TagResponse

router = APIRouter(prefix="/tags", tags=["\u6807\u7b7e"])

@router.get("", response_model=list[TagResponse])
def list_tags(db: Session = Depends(get_db)):
    tags = db.query(Tag, func.count(post_tags.c.post_id).label("pc")).outerjoin(post_tags, post_tags.c.tag_id == Tag.id).group_by(Tag.id).all()
    return [TagResponse(id=t.Tag.id, name=t.Tag.name, slug=t.Tag.slug, created_at=t.Tag.created_at, post_count=t.pc) for t in tags]

@router.post("")
def create_tag(data: TagCreate, db: Session = Depends(get_db), user=Depends(get_current_active_superuser)):
    if db.query(Tag).filter(Tag.name == data.name).first():
        raise HTTPException(status_code=400, detail="\u6807\u7b7e\u540d\u5df2\u5b58\u5728")
    tag = Tag(name=data.name, slug=data.slug)
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return {"message": "\u521b\u5efa\u6210\u529f", "id": tag.id}

@router.put("/{tag_id}")
def update_tag(tag_id: int, data: TagUpdate, db: Session = Depends(get_db), user=Depends(get_current_active_superuser)):
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="\u6807\u7b7e\u4e0d\u5b58\u5728")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(tag, key, value)
    db.commit()
    return {"message": "\u66f4\u65b0\u6210\u529f"}

@router.delete("/{tag_id}")
def delete_tag(tag_id: int, db: Session = Depends(get_db), user=Depends(get_current_active_superuser)):
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="\u6807\u7b7e\u4e0d\u5b58\u5728")
    db.delete(tag)
    db.commit()
    return {"message": "\u5220\u9664\u6210\u529f"}
