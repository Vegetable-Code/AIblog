# -*- coding: utf-8 -*-
import os, re, uuid, shutil
from typing import Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from ..core.database import get_db
from ..core.deps import get_current_active_superuser
from ..models.post import Post
from ..models.tag import Tag
from ..models.user import User
from ..api.posts import _generate_summary
from ..core import storage

router = APIRouter(prefix="/posts", tags=["??"])

ALLOWED_EXTENSIONS = {".pdf"}
MAX_FILE_SIZE = 50 * 1024 * 1024


def _extract_title_from_text(text: str) -> Optional[str]:
    for line in text.split("\n"):
        line = line.strip()
        if len(line) >= 4 and len(line) <= 200:
            return line
    return None


def _get_title_from_file(filename: str) -> str:
    return os.path.splitext(os.path.basename(filename))[0]


@router.post("/import-pdf")
async def import_pdf(
    file: UploadFile = File(...),
    category_id: Optional[int] = Form(None),
    tag_ids: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),
):
    ext = os.path.splitext(file.filename or "")[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"?????????{ext}???? PDF")

    tmp_dir = None
    try:
        import fitz

        content_bytes = await file.read()
        if len(content_bytes) > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail="????????? 50MB")

        doc = fitz.open(stream=content_bytes, filetype="pdf")
        page_count = len(doc)

        uid = uuid.uuid4().hex
        tmp_dir = storage.create_temp_dir()

        # Save original PDF to temp
        pdf_path = os.path.join(tmp_dir, "original.pdf")
        with open(pdf_path, "wb") as f:
            f.write(content_bytes)

        page_urls = []
        full_text_parts = []
        for page_num in range(page_count):
            page = doc[page_num]
            text = page.get_text()
            full_text_parts.append(text)

            pix = page.get_pixmap(dpi=150)
            img_filename = f"page-{page_num + 1}.png"
            img_path = os.path.join(tmp_dir, img_filename)
            pix.save(img_path)

            key = f"pdfs/{uid}/{img_filename}"
            url = storage.upload_local(img_path, key)
            page_urls.append(url)

        doc.close()
        full_text = "\n".join(full_text_parts).strip()

        if not page_urls:
            raise HTTPException(status_code=400, detail="PDF ??????")

        # Upload original PDF
        pdf_key = f"pdfs/{uid}/original.pdf"
        pdf_url = storage.upload_local(pdf_path, pdf_key)

        html_parts = []
        for idx, img_url in enumerate(page_urls):
            html_parts.append('<div class="pdf-page">')
            html_parts.append(f'  <img src="{img_url}" alt="? {idx+1} ?" style="max-width:100%;height:auto;margin-bottom:1rem;border-radius:4px;box-shadow:0 2px 8px rgba(0,0,0,0.1);" />')
            html_parts.append('</div>')
        html_parts.append('<p class="pdf-download" style="margin-top:2rem;padding-top:1rem;border-top:1px solid #e2e8f0;">')
        html_parts.append(f'  <a href="{pdf_url}" download style="display:inline-flex;align-items:center;gap:0.5rem;padding:0.75rem 1.5rem;background:#1e293b;color:white;border-radius:8px;text-decoration:none;font-weight:500;">')
        html_parts.append('    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>')
        html_parts.append('    ???? PDF')
        html_parts.append('  </a>')
        html_parts.append('</p>')
        content_html = "\n".join(html_parts)

        title = doc.metadata.get("title", "").strip()
        if not title:
            title = _extract_title_from_text(full_text)
        if not title:
            title = _get_title_from_file(file.filename or "untitled")

        from ..api.posts import _generate_summary
        summary = _generate_summary(full_text)

        slug = re.sub(r"-+", "-", re.sub(r"[^a-z0-9\u4e00-\u9fa5]+", "-", title.lower())).strip("-")
        if not slug:
            slug = f"post-{uuid.uuid4().hex[:8]}"
        existing = db.query(Post).filter(Post.slug == slug).first()
        if existing:
            slug = f"{slug}-{uuid.uuid4().hex[:4]}"

        parsed_tag_ids = []
        if tag_ids:
            try:
                parsed_tag_ids = [int(x.strip()) for x in tag_ids.split(",") if x.strip()]
            except ValueError:
                pass

        post = Post(
            title=title,
            slug=slug,
            summary=summary,
            content=full_text,
            content_html=content_html,
            cover_image=page_urls[0] if page_urls else "",
            is_published=True,
            is_top=False,
            category_id=category_id,
            author_id=current_user.id,
            published_at=datetime.now(timezone.utc),
        )

        if parsed_tag_ids:
            tags = db.query(Tag).filter(Tag.id.in_(parsed_tag_ids)).all()
            post.tags = tags

        db.add(post)
        db.commit()
        db.refresh(post)

        return {
            "message": "????",
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
        raise HTTPException(status_code=500, detail=f"PDF ?????{str(e)}")
    finally:
        if tmp_dir and os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir, ignore_errors=True)
