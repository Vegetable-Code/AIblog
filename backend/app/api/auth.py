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
from pydantic import BaseModel, EmailStr
from ..schemas.user import UserResponse

router = APIRouter(prefix="/auth", tags=["认证"])


class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    nickname: str = ""
    email_code: str
    captcha_id: str
    captcha_text: str


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="账号已被禁用")
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return Token(access_token=access_token)


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/register", response_model=UserResponse)
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    from .captcha import verify_captcha
    if not verify_captcha(req.captcha_id, req.captcha_text):
        raise HTTPException(status_code=400, detail="图形验证码错误")

    from .email_code import verify_email_code
    if not verify_email_code(req.email, req.email_code):
        raise HTTPException(status_code=400, detail="邮箱验证码错误或已过期")

    db_user = db.query(User).filter((User.username == req.username) | (User.email == req.email)).first()
    if db_user:
        raise HTTPException(status_code=400, detail="用户名或邮箱已存在")
    user = User(
        username=req.username,
        email=req.email,
        hashed_password=get_password_hash(req.password),
        nickname=req.nickname or req.username
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
