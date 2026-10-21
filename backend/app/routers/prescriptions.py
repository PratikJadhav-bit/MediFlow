"""Prescriptions API."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from datetime import date
from app.database import get_db
from app.models.models import Prescription, PrescriptionItem
from app.schemas.schemas import PrescriptionCreate, PrescriptionResponse

router = APIRouter()

@router.get("/", response_model=List[PrescriptionResponse])
def list_prescriptions(status: str = None, db: Session = Depends(get_db)):
    q = db.query(Prescription).options(joinedload(Prescription.patient), joinedload(Prescription.items).joinedload(PrescriptionItem.medicine))
    if status: q = q.filter(Prescription.status == status)
    return q.order_by(Prescription.created_at.desc()).limit(50).all()

@router.get("/{rx_id}", response_model=PrescriptionResponse)
def get_prescription(rx_id: int, db: Session = Depends(get_db)):
    rx = db.query(Prescription).options(joinedload(Prescription.patient), joinedload(Prescription.items).joinedload(PrescriptionItem.medicine)).filter(Prescription.id == rx_id).first()
    if not rx: raise HTTPException(404, "Prescription not found")
    return rx

@router.post("/", response_model=PrescriptionResponse, status_code=201)
def create_prescription(payload: PrescriptionCreate, db: Session = Depends(get_db)):
    count = db.query(Prescription).count()
    rx = Prescription(
        rx_number=f"RX-{date.today().year}-{count+1:04d}",
        patient_id=payload.patient_id, doctor_name=payload.doctor_name,
        doctor_reg=payload.doctor_reg, hospital=payload.hospital,
        notes=payload.notes, prescribed_date=payload.prescribed_date or date.today()
    )
    db.add(rx); db.flush()
    for item in payload.items:
        db.add(PrescriptionItem(prescription_id=rx.id, **item.model_dump()))
    db.commit(); db.refresh(rx)
    return rx

@router.patch("/{rx_id}/dispense")
def dispense_prescription(rx_id: int, db: Session = Depends(get_db)):
    rx = db.query(Prescription).filter(Prescription.id == rx_id).first()
    if not rx: raise HTTPException(404, "Prescription not found")
    rx.status = "dispensed"
    rx.dispensed_date = date.today()
    db.commit()
    return {"message": "Prescription dispensed successfully", "rx_number": rx.rx_number}
