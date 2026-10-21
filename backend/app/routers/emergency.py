from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Medicine

router = APIRouter()

@router.get("/")
def emergency_stock(db: Session = Depends(get_db)):
    meds = db.query(Medicine).filter(Medicine.is_emergency == True, Medicine.is_active == True).all()
    return [
        {
            "id": m.id, "name": m.name, "code": m.code,
            "stock": m.stock_qty, "min_required": m.min_stock,
            "location": m.location, "expiry_date": str(m.expiry_date),
            "status": m.stock_status, "days_to_expiry": m.days_to_expiry,
        }
        for m in meds
    ]
