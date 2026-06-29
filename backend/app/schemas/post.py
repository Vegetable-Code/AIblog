from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from .category import CategoryResponse
from .tag import TagResponse


class PostBase(BaseModel):
    title: str
    slug: str
    summary: Optional[str] = ""
    content: str
    cover_image: Optional[str] = ""
    is_published: Optional[bool] = False
    is_top: Optional[bool] = False
    category_id: Optional[int] = None
    tag_ids: Optional[List[int]] = []


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    summary: Optional[str] = None
    content: Optional[str] = None
    cover_image: Optional[str] = None
    is_published: Optional[bool] = None
    is_top: Optional[bool] = None
    category_id: Optional[int] = None
    tag_ids: Optional[List[int]] = None


class PostListItem(BaseModel):
    id: int
    title: str
    slug: str
    summary: Optional[str] = ""
    cover_image: Optional[str] = ""
    is_published: bool
    is_top: bool
    views_count: int
    category: Optional[CategoryResponse] = None
    tags: List[TagResponse] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    published_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class PostDetail(PostListItem):
    content: str
    content_html: Optional[str] = ""

    class Config:
        from_attributes = True


class PostPage(BaseModel):
    items: List[PostListItem]
    total: int
    page: int
    page_size: int
    total_pages: int
