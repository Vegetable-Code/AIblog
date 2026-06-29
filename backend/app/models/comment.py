from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from ..core.database import Base


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    nickname = Column(String(50), default="匿名")
    email = Column(String(100), default="")
    website = Column(String(500), default="")
    is_approved = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    parent_id = Column(Integer, ForeignKey("comments.id", ondelete="CASCADE"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    author = relationship("User", backref="comments")
    post = relationship("Post", backref="comments")
    replies = relationship("Comment", backref="parent", remote_side=[id], lazy="select")
