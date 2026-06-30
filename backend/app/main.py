from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .core.database import get_db
from .core.database import engine, Base
from .api import auth, posts, categories, tags, comments, users, dashboard, ai_search, captcha, email_code
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
app.include_router(email_code.router, prefix=api_prefix)
app.include_router(detail_router, prefix=api_prefix)

@app.get("/")
def root():
    return {"message": "Blog API is running", "version": settings.VERSION}
