from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Reminder, Patient
from app.schemas.schemas import ReminderCreate, ReminderResponse
from typing import List

router = APIRouter()

@router.get("/", response_model=List[ReminderResponse])
def list_reminders(db: Session = Depends(get_db)):
    from sqlalchemy.orm import joinedload
    return db.query(Reminder).options(joinedload(Reminder.patient)).all()

@router.post("/", response_model=ReminderResponse, status_code=201)
def create_reminder(payload: ReminderCreate, db: Session = Depends(get_db)):
    r = Reminder(**payload.model_dump())
    db.add(r); db.commit(); db.refresh(r)
    return r

@router.patch("/{reminder_id}/toggle")
def toggle_reminder(reminder_id: int, db: Session = Depends(get_db)):
    r = db.query(Reminder).filter(Reminder.id == reminder_id).first()
    if not r: return {"error": "Not found"}
    r.is_active = not r.is_active
    db.commit()
    return {"id": r.id, "is_active": r.is_active}
