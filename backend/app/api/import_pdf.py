# -*- coding: utf-8 -*-
import os, re, uuid
from typing import Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from ..core.database import get_db
from ..core.deps import get_current_active_superuser
from ..models.post import Post
from ..models.tag import Tag
from ..models.user import User
from ..api.posts import _md_to_html, _generate_summary

router = APIRouter(prefix="/posts", tags=["文章"])

ALLOWED_EXTENSIONS = {".pdf"}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB


def _extract_title_from_text(text: str) -> Optional[str]:
    """从提取的文本中推断标题：取第一个有意义的行。"""
    for line in text.split("\n"):
        line = line.strip()
        if len(line) >= 4 and len(line) <= 200:
            return line
    return None


def _get_title_from_file(filename: str) -> str:
    """从文件名去掉扩展名作为标题。"""
    return os.path.splitext(os.path.basename(filename))[0]


@router.post("/import-pdf")
async def import_pdf(
    file: UploadFile = File(...),
    category_id: Optional[int] = Form(None),
    tag_ids: Optional[str] = Form(None),  # comma-separated IDs
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),
):
    """Import a PDF file and create a blog post from its content."""
    # Validate file extension
    ext = os.path.splitext(file.filename or "")[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"不支持的文件格式：{ext}，仅支持 PDF")

    # Save uploaded file to temp location
    try:
        import fitz  # PyMuPDF

        content_bytes = await file.read()
        if len(content_bytes) > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail="文件过大，最大支持 50MB")

        # Extract text using PyMuPDF
        doc = fitz.open(stream=content_bytes, filetype="pdf")
        full_text_parts = []
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text()
            full_text_parts.append(text)

        full_text = "\n".join(full_text_parts).strip()

        if not full_text:
            raise HTTPException(status_code=400, detail="未能从 PDF 中提取到任何文本内容")

        # Determine title
        title = doc.metadata.get("title", "").strip()
        if not title:
            title = _extract_title_from_text(full_text)
        if not title:
            title = _get_title_from_file(file.filename or "untitled")

        # Generate slug
        slug = re.sub(r'-+', '-', re.sub(r'[^a-z0-9\u4e00-\u9fa5]+', '-', title.lower())).strip('-')
        if not slug:
            slug = f"post-{uuid.uuid4().hex[:8]}"

        # Handle duplicate slug
        existing = db.query(Post).filter(Post.slug == slug).first()
        if existing:
            slug = f"{slug}-{uuid.uuid4().hex[:4]}"

        # Generate content_html and summary
        content_html = _md_to_html(full_text)
        summary = _generate_summary(full_text)

        # Parse tag_ids
        parsed_tag_ids = []
        if tag_ids:
            try:
                parsed_tag_ids = [int(x.strip()) for x in tag_ids.split(",") if x.strip()]
            except ValueError:
                pass

        # Create the post
        post = Post(
            title=title,
            slug=slug,
            summary=summary,
            content=full_text,
            content_html=content_html,
            cover_image="",
            is_published=False,
            is_top=False,
            category_id=category_id,
            author_id=current_user.id,
            published_at=None,
        )

        if parsed_tag_ids:
            tags = db.query(Tag).filter(Tag.id.in_(parsed_tag_ids)).all()
            post.tags = tags

        db.add(post)
        db.commit()
        db.refresh(post)

        page_count = len(doc)
        doc.close()

        return {
            "message": "导入成功",
            "id": post.id,
            "title": post.title,
            "slug": post.slug,
            "summary": post.summary,
            "pages": page_count,
            "char_count": len(full_text),
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF 导入失败：{str(e)}")