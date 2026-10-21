from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload
from app.database import get_db
from app.models.models import Delivery

router = APIRouter()

@router.get("/")
def list_deliveries(db: Session = Depends(get_db)):
    return db.query(Delivery).options(joinedload(Delivery.order)).all()

@router.patch("/{delivery_id}/step")
def advance_delivery_step(delivery_id: int, db: Session = Depends(get_db)):
    d = db.query(Delivery).filter(Delivery.id == delivery_id).first()
    if not d: return {"error": "Not found"}
    d.current_step = min(d.current_step + 1, 3)
    if d.current_step == 3:
        d.status = "delivered"
        d.order.status = "delivered"
    db.commit()
    return {"step": d.current_step, "status": d.status}
