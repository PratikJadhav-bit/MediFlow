"""Orders, Reminders, Deliveries, Branches, Emergency, AI, and Forecast routers."""
# orders.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from datetime import datetime
from app.database import get_db
from app.models.models import Order, OrderItem
from app.schemas.schemas import OrderCreate, OrderResponse

router = APIRouter()

@router.get("/", response_model=List[OrderResponse])
def list_orders(status: str = None, limit: int = 50, db: Session = Depends(get_db)):
    q = db.query(Order).options(joinedload(Order.patient), joinedload(Order.items).joinedload(OrderItem.medicine))
    if status: q = q.filter(Order.status == status)
    return q.order_by(Order.created_at.desc()).limit(limit).all()

@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    o = db.query(Order).options(joinedload(Order.patient), joinedload(Order.items)).filter(Order.id == order_id).first()
    if not o: raise HTTPException(404, "Order not found")
    return o

@router.patch("/{order_id}/status")
def update_order_status(order_id: int, status: str, db: Session = Depends(get_db)):
    o = db.query(Order).filter(Order.id == order_id).first()
    if not o: raise HTTPException(404, "Order not found")
    o.status = status
    if status == "delivered": o.is_paid = True
    db.commit()
    return {"message": f"Order {o.order_number} status updated to {status}"}
