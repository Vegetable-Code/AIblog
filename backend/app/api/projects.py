from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
import os, uuid
from ..core.database import get_db
from ..core.deps import get_current_active_superuser
from ..models.project import Project
from ..schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse

router = APIRouter(prefix="/projects", tags=["作品"])

# ---------- public (前台用) ----------
@router.get("/public", response_model=List[ProjectResponse])
def list_public_projects(db: Session = Depends(get_db)):
    return db.query(Project).filter(Project.is_published == True).order_by(Project.sort_order.asc(), Project.created_at.desc()).all()

@router.get("/public/{slug}", response_model=ProjectResponse)
def get_public_project(slug: str, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.slug == slug, Project.is_published == True).first()
    if not project:
        raise HTTPException(status_code=404, detail="作品不存在")
    return project

# ---------- admin ----------
@router.get("", response_model=List[ProjectResponse])
def list_projects(db: Session = Depends(get_db), user=Depends(get_current_active_superuser)):
    return db.query(Project).order_by(Project.sort_order.asc(), Project.created_at.desc()).all()

@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db), user=Depends(get_current_active_superuser)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="作品不存在")
    return project

@router.post("", response_model=ProjectResponse)
def create_project(req: ProjectCreate, db: Session = Depends(get_db), user=Depends(get_current_active_superuser)):
    if db.query(Project).filter(Project.slug == req.slug).first():
        raise HTTPException(status_code=400, detail="Slug 已存在")
    project = Project(**req.model_dump())
    db.add(project)
    db.commit()
    db.refresh(project)
    return project

@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(project_id: int, req: ProjectUpdate, db: Session = Depends(get_db), user=Depends(get_current_active_superuser)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="作品不存在")
    update_data = req.model_dump(exclude_unset=True)
    if "slug" in update_data and update_data["slug"] != project.slug:
        if db.query(Project).filter(Project.slug == update_data["slug"]).first():
            raise HTTPException(status_code=400, detail="Slug 已存在")
    for key, value in update_data.items():
        setattr(project, key, value)
    db.commit()
    db.refresh(project)
    return project

@router.delete("/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db), user=Depends(get_current_active_superuser)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="作品不存在")
    db.delete(project)
    db.commit()
    return {"message": "删除成功"}

# ---------- image upload ----------
UPLOAD_DIR = os.environ.get("UPLOAD_ROOT", "uploads")
PROJECT_IMG_DIR = os.path.join(UPLOAD_DIR, "projects")

@router.post("/upload")
def upload_project_image(file: UploadFile = File(...), user=Depends(get_current_active_superuser)):
    os.makedirs(PROJECT_IMG_DIR, exist_ok=True)
    ext = file.filename.rsplit(".", 1)[-1] if "." in (file.filename or "") else "png"
    fname = f"project_{uuid.uuid4().hex[:12]}.{ext}"
    fpath = os.path.join(PROJECT_IMG_DIR, fname)
    with open(fpath, "wb") as f:
        f.write(file.file.read())
    return {"url": f"/uploads/projects/{fname}"}
