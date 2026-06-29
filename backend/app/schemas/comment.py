from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class CommentBase(BaseModel):
    content: str
    nickname: Optional[str] = "匿名"
    email: Optional[str] = ""
    website: Optional[str] = ""


class CommentCreate(CommentBase):
    post_id: int
    parent_id: Optional[int] = None


class CommentUpdate(BaseModel):
    content: Optional[str] = None
    is_approved: Optional[bool] = None


class CommentResponse(BaseModel):
    id: int
    content: str
    nickname: str
    email: str
    website: str
    is_approved: bool
    post_id: int
    parent_id: Optional[int] = None
    created_at: Optional[datetime] = None
    replies: List["CommentResponse"] = []

    class Config:
        from_attributes = True
