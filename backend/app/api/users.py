from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..core.security import get_password_hash
from ..core.deps import get_current_active_superuser
from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate

router = APIRouter(prefix="/users", tags=["\u7528\u6237"])

@router.get("")
def list_users(page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100),
               db: Session = Depends(get_db), user=Depends(get_current_active_superuser)):
    query = db.query(User).order_by(User.created_at.desc())
    total = query.count()
    users = query.offset((page - 1) * page_size).limit(page_size).all()
    return {"items": users, "total": total, "page": page, "page_size": page_size, "total_pages": (total + page_size - 1) // page_size}

@router.post("")
def create_user(data: UserCreate, db: Session = Depends(get_db), user=Depends(get_current_active_superuser)):
    if db.query(User).filter((User.username == data.username) | (User.email == data.email)).first():
        raise HTTPException(status_code=400, detail="\u7528\u6237\u540d\u6216\u90ae\u7bb1\u5df2\u5b58\u5728")
    new_user = User(username=data.username, email=data.email, hashed_password=get_password_hash(data.password),
                    nickname=data.nickname or "", avatar=data.avatar or "", is_active=True)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "\u521b\u5efa\u6210\u529f", "id": new_user.id}

@router.put("/{user_id}")
def update_user(user_id: int, data: UserUpdate, db: Session = Depends(get_db), user=Depends(get_current_active_superuser)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="\u7528\u6237\u4e0d\u5b58\u5728")
    update_data = data.model_dump(exclude_unset=True)
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
    for key, value in update_data.items():
        setattr(db_user, key, value)
    db.commit()
    return {"message": "\u66f4\u65b0\u6210\u529f"}

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), user=Depends(get_current_active_superuser)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="\u7528\u6237\u4e0d\u5b58\u5728")
    if db_user.is_superuser:
        raise HTTPException(status_code=400, detail="\u4e0d\u80fd\u5220\u9664\u8d85\u7ea7\u7ba1\u7406\u5458")
    db.delete(db_user)
    db.commit()
    return {"message": "\u5220\u9664\u6210\u529f"}
