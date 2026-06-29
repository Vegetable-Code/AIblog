from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..core.database import get_db
from ..core.deps import get_current_active_superuser
from ..models.category import Category
from ..models.post import Post
from ..schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse

router = APIRouter(prefix="/categories", tags=["\u5206\u7c7b"])

@router.get("", response_model=list[CategoryResponse])
def list_categories(db: Session = Depends(get_db)):
    cats = db.query(Category, func.count(Post.id).label("pc")).outerjoin(Post, Post.category_id == Category.id).group_by(Category.id).all()
    return [CategoryResponse(id=c.Category.id, name=c.Category.name, slug=c.Category.slug,
            description=c.Category.description or "", created_at=c.Category.created_at, post_count=c.pc) for c in cats]

@router.post("")
def create_category(data: CategoryCreate, db: Session = Depends(get_db), user=Depends(get_current_active_superuser)):
    if db.query(Category).filter(Category.name == data.name).first():
        raise HTTPException(status_code=400, detail="\u5206\u7c7b\u540d\u5df2\u5b58\u5728")
    cat = Category(name=data.name, slug=data.slug, description=data.description or "")
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return {"message": "\u521b\u5efa\u6210\u529f", "id": cat.id}

@router.put("/{category_id}")
def update_category(category_id: int, data: CategoryUpdate, db: Session = Depends(get_db), user=Depends(get_current_active_superuser)):
    cat = db.query(Category).filter(Category.id == category_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="\u5206\u7c7b\u4e0d\u5b58\u5728")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(cat, key, value)
    db.commit()
    return {"message": "\u66f4\u65b0\u6210\u529f"}

@router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db), user=Depends(get_current_active_superuser)):
    cat = db.query(Category).filter(Category.id == category_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="\u5206\u7c7b\u4e0d\u5b58\u5728")
    if db.query(Post).filter(Post.category_id == category_id).first():
        raise HTTPException(status_code=400, detail="\u8be5\u5206\u7c7b\u4e0b\u8fd8\u6709\u6587\u7ae0\uff0c\u65e0\u6cd5\u5220\u9664")
    db.delete(cat)
    db.commit()
    return {"message": "\u5220\u9664\u6210\u529f"}
