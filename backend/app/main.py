from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
import os
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .core.database import get_db
from .core.database import engine, Base
from .api import auth, posts, categories, tags, comments, users, dashboard, ai_search, captcha
from .api import import_pdf
from .api.posts import detail_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION, description="Blog API")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

api_prefix = settings.API_V1_STR
app.include_router(auth.router, prefix=api_prefix)
app.include_router(posts.router, prefix=api_prefix)
app.include_router(categories.router, prefix=api_prefix)
app.include_router(tags.router, prefix=api_prefix)
app.include_router(comments.router, prefix=api_prefix)
app.include_router(users.router, prefix=api_prefix)
app.include_router(dashboard.router, prefix=api_prefix)
app.include_router(ai_search.router, prefix=api_prefix)
app.include_router(captcha.router, prefix=api_prefix)
app.include_router(import_pdf.router, prefix=api_prefix)
app.include_router(detail_router, prefix=api_prefix)

# Mount uploads directory (for local dev without Nginx)
_uploads_dir = os.environ.get("UPLOAD_ROOT", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "uploads"))
if os.path.exists(_uploads_dir):
    app.mount("/uploads", StaticFiles(directory=_uploads_dir), name="uploads")


@app.get("/")
def root():
    return {"message": "Blog API is running", "version": settings.VERSION}
