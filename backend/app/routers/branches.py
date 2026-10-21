from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Branch

router = APIRouter()

@router.get("/")
def list_branches(db: Session = Depends(get_db)):
    return db.query(Branch).all()

@router.get("/{branch_id}")
def get_branch(branch_id: int, db: Session = Depends(get_db)):
    return db.query(Branch).filter(Branch.id == branch_id).first()
