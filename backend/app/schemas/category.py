from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CategoryBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = ""


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None


class CategoryResponse(CategoryBase):
    id: int
    created_at: Optional[datetime] = None
    post_count: Optional[int] = 0

    class Config:
        from_attributes = True
