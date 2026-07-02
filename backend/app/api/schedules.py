from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..core.deps import get_current_user
from ..models.user import User
from ..models.schedule import Schedule
from ..schemas.schedule import ScheduleCreate, ScheduleUpdate, ScheduleResponse

router = APIRouter(prefix="/schedules", tags=["日程"])

@router.get("/today", response_model=List[ScheduleResponse])
def get_today_schedules(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    today = date.today()
    schedules = db.query(Schedule).filter(
        Schedule.user_id == current_user.id,
        Schedule.date == today
    ).order_by(Schedule.created_at.asc()).all()
    return schedules

@router.get("", response_model=List[ScheduleResponse])
def get_schedules_by_date(
    date_str: str = Query(..., description="YYYY-MM-DD"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        query_date = date.fromisoformat(date_str)
    except ValueError:
        raise HTTPException(status_code=400, detail="日期格式不正确，请使用 YYYY-MM-DD")
    schedules = db.query(Schedule).filter(
        Schedule.user_id == current_user.id,
        Schedule.date == query_date
    ).order_by(Schedule.created_at.asc()).all()
    return schedules

@router.post("", response_model=ScheduleResponse)
def create_schedule(
    req: ScheduleCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        schedule_date = date.fromisoformat(req.date)
    except ValueError:
        raise HTTPException(status_code=400, detail="日期格式不正确，请使用 YYYY-MM-DD")
    schedule = Schedule(
        user_id=current_user.id,
        date=schedule_date,
        title=req.title,
        description=req.description,
    )
    db.add(schedule)
    db.commit()
    db.refresh(schedule)
    return schedule

@router.put("/{schedule_id}", response_model=ScheduleResponse)
def update_schedule(
    schedule_id: int,
    req: ScheduleUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    schedule = db.query(Schedule).filter(Schedule.id == schedule_id, Schedule.user_id == current_user.id).first()
    if not schedule:
        raise HTTPException(status_code=404, detail="日程不存在")
    if req.title is not None:
        schedule.title = req.title
    if req.description is not None:
        schedule.description = req.description
    if req.is_completed is not None:
        schedule.is_completed = req.is_completed
    db.commit()
    db.refresh(schedule)
    return schedule

@router.delete("/{schedule_id}")
def delete_schedule(
    schedule_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    schedule = db.query(Schedule).filter(Schedule.id == schedule_id, Schedule.user_id == current_user.id).first()
    if not schedule:
        raise HTTPException(status_code=404, detail="日程不存在")
    db.delete(schedule)
    db.commit()
    return {"message": "删除成功"}
