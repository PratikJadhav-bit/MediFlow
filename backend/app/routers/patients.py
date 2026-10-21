"""Patients CRUD API."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from app.database import get_db
from app.models.models import Patient, Prescription, Order
from app.schemas.schemas import PatientCreate, PatientResponse

router = APIRouter()

@router.get("/", response_model=List[PatientResponse])
def list_patients(search: Optional[str] = None, limit: int = 100, db: Session = Depends(get_db)):
    q = db.query(Patient).filter(Patient.is_active == True)
    if search:
        q = q.filter(or_(Patient.name.ilike(f"%{search}%"), Patient.phone.ilike(f"%{search}%")))
    return q.limit(limit).all()

@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    p = db.query(Patient).filter(Patient.id == patient_id).first()
    if not p: raise HTTPException(404, "Patient not found")
    return p

@router.get("/{patient_id}/history")
def patient_history(patient_id: int, db: Session = Depends(get_db)):
    orders = db.query(Order).filter(Order.patient_id == patient_id).order_by(Order.created_at.desc()).all()
    prescriptions = db.query(Prescription).filter(Prescription.patient_id == patient_id).order_by(Prescription.created_at.desc()).all()
    return {
        "orders": [{"id": o.id, "order_number": o.order_number, "total": o.total, "status": o.status, "created_at": str(o.created_at)} for o in orders],
        "prescriptions": [{"id": p.id, "rx_number": p.rx_number, "doctor": p.doctor_name, "status": p.status, "date": str(p.prescribed_date)} for p in prescriptions],
    }

@router.post("/", response_model=PatientResponse, status_code=201)
def create_patient(payload: PatientCreate, db: Session = Depends(get_db)):
    count = db.query(Patient).count()
    p = Patient(**payload.model_dump(), patient_code=f"P{count+1:04d}")
    db.add(p); db.commit(); db.refresh(p)
    return p
