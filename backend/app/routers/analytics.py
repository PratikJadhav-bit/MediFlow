"""Analytics and dashboard statistics API."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from datetime import date, datetime, timedelta

from app.database import get_db
from app.models.models import Medicine, Patient, Order, Prescription, Delivery, SalesRecord
from app.schemas.schemas import DashboardStats, SalesTrend

router = APIRouter()


@router.get("/dashboard", response_model=DashboardStats, summary="Get dashboard KPI stats")
def dashboard_stats(db: Session = Depends(get_db)):
    today = date.today()
    return DashboardStats(
        total_medicines=db.query(Medicine).filter(Medicine.is_active == True).count(),
        total_patients=db.query(Patient).filter(Patient.is_active == True).count(),
        today_orders=db.query(Order).filter(
            func.date(Order.created_at) == today
        ).count(),
        today_revenue=db.query(func.sum(Order.total)).filter(
            func.date(Order.created_at) == today,
            Order.is_paid == True
        ).scalar() or 0.0,
        low_stock_count=db.query(Medicine).filter(
            Medicine.is_active == True,
            Medicine.stock_qty < Medicine.min_stock
        ).count(),
        expiring_soon_count=db.query(Medicine).filter(
            Medicine.is_active == True,
            Medicine.expiry_date != None,
            Medicine.expiry_date <= today + timedelta(days=30)
        ).count(),
        pending_prescriptions=db.query(Prescription).filter(
            Prescription.status == "pending"
        ).count(),
        active_deliveries=db.query(Delivery).filter(
            Delivery.status.in_(["assigned", "picked_up", "in_transit"])
        ).count(),
    )


@router.get("/sales-trend", summary="Monthly sales trend")
def sales_trend(months: int = 12, db: Session = Depends(get_db)):
    records = db.query(SalesRecord).filter(
        SalesRecord.date >= date.today().replace(day=1) - timedelta(days=months * 31)
    ).all()

    month_data: dict = {}
    for r in records:
        key = r.date.strftime("%b %Y")
        if key not in month_data:
            month_data[key] = {"revenue": 0.0, "orders": 0}
        month_data[key]["revenue"] += r.revenue
        month_data[key]["orders"] += r.orders_count

    labels = list(month_data.keys())[-12:]
    revenue = [round(month_data[k]["revenue"], 2) for k in labels]
    orders  = [month_data[k]["orders"] for k in labels]

    return {"labels": labels, "revenue": revenue, "orders": orders}


@router.get("/category-breakdown", summary="Revenue breakdown by medicine category")
def category_breakdown(db: Session = Depends(get_db)):
    records = db.query(
        SalesRecord.category,
        func.sum(SalesRecord.revenue).label("total")
    ).group_by(SalesRecord.category).all()

    return {
        "labels": [r.category for r in records],
        "values": [round(r.total, 2) for r in records],
    }


@router.get("/top-medicines", summary="Top selling medicines")
def top_medicines(db: Session = Depends(get_db)):
    from app.models.models import OrderItem
    results = db.query(
        Medicine.name,
        func.sum(OrderItem.quantity).label("total_units"),
        func.sum(OrderItem.total).label("total_revenue"),
    ).join(OrderItem).group_by(Medicine.id).order_by(
        func.sum(OrderItem.total).desc()
    ).limit(8).all()

    return [
        {"name": r.name, "units": r.total_units or 0, "revenue": round(r.total_revenue or 0, 2)}
        for r in results
    ]


@router.get("/kpi-summary", summary="Summary KPIs for the analytics page")
def kpi_summary(db: Session = Depends(get_db)):
    today = date.today()
    month_start = today.replace(day=1)

    month_revenue = db.query(func.sum(SalesRecord.revenue)).filter(
        SalesRecord.date >= month_start
    ).scalar() or 0

    total_orders = db.query(Order).count()
    avg_order = db.query(func.avg(Order.total)).scalar() or 0

    return {
        "month_revenue": round(month_revenue, 2),
        "total_orders": total_orders,
        "avg_order_value": round(avg_order, 2),
        "total_medicines": db.query(Medicine).filter(Medicine.is_active == True).count(),
        "total_patients": db.query(Patient).filter(Patient.is_active == True).count(),
    }
