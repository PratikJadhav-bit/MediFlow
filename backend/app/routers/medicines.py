"""Medicine inventory CRUD API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from typing import List, Optional
from datetime import date, timedelta

from app.database import get_db
from app.models.models import Medicine
from app.schemas.schemas import MedicineCreate, MedicineUpdate, MedicineResponse

router = APIRouter()


@router.get("/", response_model=List[MedicineResponse], summary="List all medicines")
def list_medicines(
    search: Optional[str] = Query(None, description="Search by name or category"),
    category: Optional[str] = Query(None),
    stock_status: Optional[str] = Query(None, description="ok | low | critical | out"),
    limit: int = Query(100, le=500),
    offset: int = Query(0),
    db: Session = Depends(get_db),
):
    q = db.query(Medicine).filter(Medicine.is_active == True)
    if search:
        q = q.filter(or_(
            Medicine.name.ilike(f"%{search}%"),
            Medicine.generic_name.ilike(f"%{search}%"),
            Medicine.category.ilike(f"%{search}%"),
            Medicine.code.ilike(f"%{search}%"),
        ))
    if category:
        q = q.filter(Medicine.category.ilike(f"%{category}%"))

    meds = q.offset(offset).limit(limit).all()

    # Apply stock_status filter in Python (computed property)
    if stock_status:
        meds = [m for m in meds if m.stock_status == stock_status]

    return meds


@router.get("/expiring", response_model=List[MedicineResponse], summary="Get expiring medicines")
def expiring_medicines(days: int = Query(30), db: Session = Depends(get_db)):
    cutoff = date.today() + timedelta(days=days)
    meds = db.query(Medicine).filter(
        Medicine.is_active == True,
        Medicine.expiry_date != None,
        Medicine.expiry_date <= cutoff,
    ).order_by(Medicine.expiry_date).all()
    return meds


@router.get("/low-stock", response_model=List[MedicineResponse], summary="Get low stock medicines")
def low_stock_medicines(db: Session = Depends(get_db)):
    meds = db.query(Medicine).filter(
        Medicine.is_active == True,
        Medicine.stock_qty < Medicine.min_stock,
    ).order_by(Medicine.stock_qty).all()
    return meds


@router.get("/emergency", response_model=List[MedicineResponse], summary="Get emergency medicines")
def emergency_medicines(db: Session = Depends(get_db)):
    return db.query(Medicine).filter(
        Medicine.is_emergency == True,
        Medicine.is_active == True,
    ).all()


@router.get("/categories", summary="Get distinct medicine categories")
def get_categories(db: Session = Depends(get_db)):
    cats = db.query(Medicine.category).distinct().all()
    return [c[0] for c in cats if c[0]]


@router.get("/{medicine_id}", response_model=MedicineResponse)
def get_medicine(medicine_id: int, db: Session = Depends(get_db)):
    med = db.query(Medicine).filter(Medicine.id == medicine_id).first()
    if not med:
        raise HTTPException(status_code=404, detail="Medicine not found")
    return med


@router.post("/", response_model=MedicineResponse, status_code=201)
def create_medicine(payload: MedicineCreate, db: Session = Depends(get_db)):
    count = db.query(Medicine).count()
    code = f"M{count+1:03d}"
    med = Medicine(**payload.model_dump(), code=code)
    db.add(med)
    db.commit()
    db.refresh(med)
    return med


@router.patch("/{medicine_id}", response_model=MedicineResponse)
def update_medicine(medicine_id: int, payload: MedicineUpdate, db: Session = Depends(get_db)):
    med = db.query(Medicine).filter(Medicine.id == medicine_id).first()
    if not med:
        raise HTTPException(status_code=404, detail="Medicine not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(med, field, value)
    db.commit()
    db.refresh(med)
    return med


@router.delete("/{medicine_id}", status_code=204)
def delete_medicine(medicine_id: int, db: Session = Depends(get_db)):
    med = db.query(Medicine).filter(Medicine.id == medicine_id).first()
    if not med:
        raise HTTPException(status_code=404, detail="Medicine not found")
    med.is_active = False
    db.commit()
