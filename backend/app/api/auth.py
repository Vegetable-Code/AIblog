from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..core.security import verify_password, create_access_token, get_password_hash
from ..core.config import settings
from ..core.deps import get_current_user
from ..models.user import User
from ..schemas.token import Token
from ..schemas.user import UserResponse

router = APIRouter(prefix="/auth", tags=["\u8ba4\u8bc1"])

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="\u7528\u6237\u540d\u6216\u5bc6\u7801\u9519\u8bef")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="\u8d26\u53f7\u5df2\u88ab\u7981\u7528")
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return Token(access_token=access_token)

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/register", response_model=UserResponse)
def register(username: str, email: str, password: str, nickname: str = "", db: Session = Depends(get_db)):
    db_user = db.query(User).filter((User.username == username) | (User.email == email)).first()
    if db_user:
        raise HTTPException(status_code=400, detail="\u7528\u6237\u540d\u6216\u90ae\u7bb1\u5df2\u5b58\u5728")
    user = User(username=username, email=email, hashed_password=get_password_hash(password), nickname=nickname)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
