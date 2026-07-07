from fastapi import APIRouter, Depends
from fastapi.responses import PlainTextResponse, Response
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from ..core.database import get_db
from ..models.post import Post

router = APIRouter(tags=["SEO"])

SITE_URL = "https://aiblog-production-0847.up.railway.app"


@router.get("/robots.txt", response_class=PlainTextResponse)
def robots_txt():
    return PlainTextResponse(
        f"User-agent: *\n"
        f"Allow: /\n"
        f"Sitemap: {SITE_URL}/sitemap.xml\n"
    )


@router.get("/sitemap.xml", response_class=Response)
def sitemap_xml(db: Session = Depends(get_db)):
    posts = (
        db.query(Post)
        .filter(Post.is_published == True)
        .order_by(Post.published_at.desc())
        .all()
    )

    urls = []
    # Homepage
    urls.append(_url_entry(SITE_URL + "/", "1.0", "daily"))

    # Categories
    urls.append(_url_entry(SITE_URL + "/categories", "0.8", "weekly"))

    # Projects
    urls.append(_url_entry(SITE_URL + "/projects", "0.6", "weekly"))

    # About
    urls.append(_url_entry(SITE_URL + "/about", "0.5", "monthly"))

    # All published posts
    for p in posts:
        lastmod = p.updated_at or p.published_at or p.created_at
        if lastmod and lastmod.tzinfo is None:
            lastmod = lastmod.replace(tzinfo=timezone.utc)
        urls.append(_url_entry(
            f"{SITE_URL}/post/{p.slug}",
            "0.9",
            "weekly",
            lastmod.strftime("%Y-%m-%dT%H:%M:%S+00:00") if lastmod else None,
        ))

    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url in urls:
        xml += url + "\n"
    xml += "</urlset>"

    return Response(content=xml, media_type="application/xml")


def _url_entry(loc, priority, changefreq, lastmod=None):
    entry = f"  <url>\n    <loc>{loc}</loc>\n"
    entry += f"    <changefreq>{changefreq}</changefreq>\n"
    entry += f"    <priority>{priority}</priority>\n"
    if lastmod:
        entry += f"    <lastmod>{lastmod}</lastmod>\n"
    entry += "  </url>"
    return entry
