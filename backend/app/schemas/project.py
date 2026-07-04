from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class ProjectCreate(BaseModel):
    title: str
    slug: str
    description: str = ""
    content: str = ""
    cover_image: str = ""
    images: str = "[]"
    link: str = ""
    tags_str: str = ""
    is_published: bool = False
    sort_order: int = 0

class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    content: Optional[str] = None
    cover_image: Optional[str] = None
    images: Optional[str] = None
    link: Optional[str] = None
    tags_str: Optional[str] = None
    is_published: Optional[bool] = None
    sort_order: Optional[int] = None

class ProjectResponse(BaseModel):
    id: int
    title: str
    slug: str
    description: str
    content: str
    cover_image: str
    images: str
    link: str
    tags_str: str
    is_published: bool
    sort_order: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
