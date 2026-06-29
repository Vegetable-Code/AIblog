from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from ..core.database import Base
from ..models.post_tag import post_tags


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, index=True, nullable=False)
    summary = Column(String(500), default="")
    content = Column(Text, nullable=False)
    content_html = Column(Text)
    cover_image = Column(String(500), default="")
    is_published = Column(Boolean, default=False)
    is_top = Column(Boolean, default=False)
    views_count = Column(Integer, default=0)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    published_at = Column(DateTime(timezone=True), nullable=True)

    author = relationship("User", backref="posts")
    category = relationship("Category", backref="posts")
    tags = relationship("Tag", secondary=post_tags, backref="posts")
