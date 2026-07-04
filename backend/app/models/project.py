from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, func
from ..core.database import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    slug = Column(String(200), unique=True, nullable=False, index=True)
    description = Column(Text, default="")
    content = Column(Text, default="")
    cover_image = Column(String(500), default="")
    images = Column(Text, default="[]")          # JSON array of image URLs
    link = Column(String(500), default="")
    tags_str = Column(String(500), default="")    # comma-separated: "React,Vue,Python"
    is_published = Column(Boolean, default=False)
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
