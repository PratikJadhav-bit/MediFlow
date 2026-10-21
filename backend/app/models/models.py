"""
MediFlow AI — SQLAlchemy ORM Models
Normalized relational database schema
"""
from sqlalchemy import (
    Column, Integer, String, Float, Boolean, DateTime,
    ForeignKey, Text, Enum, Date
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


# ── Enums ─────────────────────────────────────────────────────
class OrderStatus(str, enum.Enum):
    new = "new"
    packing = "packing"
    ready = "ready"
    out_for_delivery = "out_for_delivery"
    delivered = "delivered"
    cancelled = "cancelled"

class OrderType(str, enum.Enum):
    delivery = "delivery"
    pickup = "pickup"

class PrescriptionStatus(str, enum.Enum):
    pending = "pending"
    dispensed = "dispensed"
    rejected = "rejected"
    expired = "expired"

class StockStatus(str, enum.Enum):
    ok = "ok"
    low = "low"
    critical = "critical"
    out = "out"

class DeliveryStatus(str, enum.Enum):
    assigned = "assigned"
    picked_up = "picked_up"
    in_transit = "in_transit"
    delivered = "delivered"
    failed = "failed"

class ReminderFrequency(str, enum.Enum):
    daily = "daily"
    twice_daily = "twice_daily"
    weekly = "weekly"
    custom = "custom"

class BranchStatus(str, enum.Enum):
    active = "active"
    warning = "warning"
    inactive = "inactive"


# ── Medicine (Inventory) ──────────────────────────────────────
class Medicine(Base):
    __tablename__ = "medicines"

    id            = Column(Integer, primary_key=True, index=True)
    code          = Column(String(20), unique=True, nullable=False, index=True)
    name          = Column(String(200), nullable=False, index=True)
    generic_name  = Column(String(200))
    category      = Column(String(100), nullable=False)
    manufacturer  = Column(String(200))
    hsn_code      = Column(String(20))
    location      = Column(String(50))                # Shelf/rack location
    unit          = Column(String(20), default="tablet")

    # Pricing
    mrp           = Column(Float, nullable=False)     # Max Retail Price
    cost_price    = Column(Float)
    discount_pct  = Column(Float, default=0.0)

    # Stock
    stock_qty     = Column(Integer, default=0)
    min_stock     = Column(Integer, default=50)
    max_stock     = Column(Integer, default=500)
    reorder_qty   = Column(Integer, default=200)

    # Dates
    expiry_date   = Column(Date)
    mfg_date      = Column(Date)
    created_at    = Column(DateTime(timezone=True), server_default=func.now())
    updated_at    = Column(DateTime(timezone=True), onupdate=func.now())

    # Flags
    requires_prescription = Column(Boolean, default=False)
    is_refrigerated       = Column(Boolean, default=False)
    is_controlled         = Column(Boolean, default=False)
    is_active             = Column(Boolean, default=True)
    is_emergency          = Column(Boolean, default=False)

    # Relationships
    prescription_items = relationship("PrescriptionItem", back_populates="medicine")
    order_items        = relationship("OrderItem", back_populates="medicine")
    restock_orders     = relationship("RestockOrder", back_populates="medicine")

    @property
    def stock_status(self) -> str:
        if self.stock_qty == 0:        return StockStatus.out
        if self.stock_qty < self.min_stock * 0.5: return StockStatus.critical
        if self.stock_qty < self.min_stock:       return StockStatus.low
        return StockStatus.ok

    @property
    def days_to_expiry(self) -> int | None:
        if not self.expiry_date: return None
        from datetime import date
        return (self.expiry_date - date.today()).days

    @property
    def margin_pct(self) -> float:
        if not self.cost_price or self.cost_price == 0: return 0
        return round((self.mrp - self.cost_price) / self.mrp * 100, 1)


# ── Patient ───────────────────────────────────────────────────
class Patient(Base):
    __tablename__ = "patients"

    id           = Column(Integer, primary_key=True, index=True)
    patient_code = Column(String(20), unique=True, index=True)
    name         = Column(String(200), nullable=False)
    age          = Column(Integer)
    gender       = Column(String(10))
    phone        = Column(String(20), index=True)
    email        = Column(String(200))
    blood_group  = Column(String(5))
    address      = Column(Text)
    conditions   = Column(Text)         # JSON string of conditions list
    allergies    = Column(Text)         # JSON string
    created_at   = Column(DateTime(timezone=True), server_default=func.now())
    is_active    = Column(Boolean, default=True)

    prescriptions = relationship("Prescription", back_populates="patient")
    orders        = relationship("Order", back_populates="patient")
    reminders     = relationship("Reminder", back_populates="patient")


# ── Prescription ──────────────────────────────────────────────
class Prescription(Base):
    __tablename__ = "prescriptions"

    id           = Column(Integer, primary_key=True, index=True)
    rx_number    = Column(String(30), unique=True, nullable=False)
    patient_id   = Column(Integer, ForeignKey("patients.id"), nullable=False)
    doctor_name  = Column(String(200))
    doctor_reg   = Column(String(50))
    hospital     = Column(String(200))
    notes        = Column(Text)
    status       = Column(String(20), default=PrescriptionStatus.pending)
    prescribed_date = Column(Date)
    dispensed_date  = Column(Date)
    created_at   = Column(DateTime(timezone=True), server_default=func.now())

    patient = relationship("Patient", back_populates="prescriptions")
    items   = relationship("PrescriptionItem", back_populates="prescription")


class PrescriptionItem(Base):
    __tablename__ = "prescription_items"

    id              = Column(Integer, primary_key=True, index=True)
    prescription_id = Column(Integer, ForeignKey("prescriptions.id"), nullable=False)
    medicine_id     = Column(Integer, ForeignKey("medicines.id"), nullable=False)
    dosage          = Column(String(100))   # e.g. "1-0-1"
    duration_days   = Column(Integer)
    instructions    = Column(Text)
    quantity        = Column(Integer)

    prescription = relationship("Prescription", back_populates="items")
    medicine     = relationship("Medicine", back_populates="prescription_items")


# ── Order ─────────────────────────────────────────────────────
class Order(Base):
    __tablename__ = "orders"

    id          = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(30), unique=True, nullable=False)
    patient_id   = Column(Integer, ForeignKey("patients.id"), nullable=False)
    branch_id    = Column(Integer, ForeignKey("branches.id"))
    status       = Column(String(30), default=OrderStatus.new)
    order_type   = Column(String(20), default=OrderType.delivery)
    subtotal     = Column(Float, default=0.0)
    discount     = Column(Float, default=0.0)
    tax          = Column(Float, default=0.0)
    total        = Column(Float, default=0.0)
    payment_method = Column(String(30), default="cash")
    is_paid      = Column(Boolean, default=False)
    notes        = Column(Text)
    delivery_address = Column(Text)
    created_at   = Column(DateTime(timezone=True), server_default=func.now())
    updated_at   = Column(DateTime(timezone=True), onupdate=func.now())

    patient  = relationship("Patient", back_populates="orders")
    branch   = relationship("Branch", back_populates="orders")
    items    = relationship("OrderItem", back_populates="order")
    delivery = relationship("Delivery", back_populates="order", uselist=False)


class OrderItem(Base):
    __tablename__ = "order_items"

    id          = Column(Integer, primary_key=True, index=True)
    order_id    = Column(Integer, ForeignKey("orders.id"), nullable=False)
    medicine_id = Column(Integer, ForeignKey("medicines.id"), nullable=False)
    quantity    = Column(Integer, nullable=False)
    unit_price  = Column(Float, nullable=False)
    discount    = Column(Float, default=0.0)
    total       = Column(Float, nullable=False)

    order    = relationship("Order", back_populates="items")
    medicine = relationship("Medicine", back_populates="order_items")


# ── Branch ────────────────────────────────────────────────────
class Branch(Base):
    __tablename__ = "branches"

    id          = Column(Integer, primary_key=True, index=True)
    branch_code = Column(String(10), unique=True, nullable=False)
    name        = Column(String(200), nullable=False)
    location    = Column(String(300))
    manager     = Column(String(200))
    phone       = Column(String(20))
    email       = Column(String(200))
    is_main     = Column(Boolean, default=False)
    status      = Column(String(20), default=BranchStatus.active)
    monthly_revenue = Column(Float, default=0.0)
    staff_count  = Column(Integer, default=0)
    created_at   = Column(DateTime(timezone=True), server_default=func.now())

    orders = relationship("Order", back_populates="branch")


# ── Drug Interaction ──────────────────────────────────────────
class DrugInteraction(Base):
    __tablename__ = "drug_interactions"

    id           = Column(Integer, primary_key=True, index=True)
    drug1        = Column(String(200), nullable=False)
    drug2        = Column(String(200), nullable=False)
    severity     = Column(String(20))    # none, mild, moderate, severe
    description  = Column(Text)
    recommendation = Column(Text)
    mechanism    = Column(Text)
    created_at   = Column(DateTime(timezone=True), server_default=func.now())


# ── Reminder (WhatsApp) ───────────────────────────────────────
class Reminder(Base):
    __tablename__ = "reminders"

    id          = Column(Integer, primary_key=True, index=True)
    patient_id  = Column(Integer, ForeignKey("patients.id"), nullable=False)
    medicine_name = Column(String(200))
    reminder_time = Column(String(10))   # HH:MM
    frequency   = Column(String(20), default=ReminderFrequency.daily)
    is_active   = Column(Boolean, default=True)
    message_template = Column(Text)
    last_sent   = Column(DateTime(timezone=True))
    created_at  = Column(DateTime(timezone=True), server_default=func.now())

    patient = relationship("Patient", back_populates="reminders")


# ── Delivery ──────────────────────────────────────────────────
class Delivery(Base):
    __tablename__ = "deliveries"

    id           = Column(Integer, primary_key=True, index=True)
    order_id     = Column(Integer, ForeignKey("orders.id"), nullable=False)
    delivery_agent = Column(String(200))
    agent_phone  = Column(String(20))
    status       = Column(String(20), default=DeliveryStatus.assigned)
    current_step = Column(Integer, default=0)   # 0=assigned,1=picked,2=transit,3=delivered
    pickup_time  = Column(DateTime(timezone=True))
    delivery_time = Column(DateTime(timezone=True))
    estimated_mins = Column(Integer)
    tracking_notes = Column(Text)
    created_at   = Column(DateTime(timezone=True), server_default=func.now())

    order = relationship("Order", back_populates="delivery")


# ── Restock Order ─────────────────────────────────────────────
class RestockOrder(Base):
    __tablename__ = "restock_orders"

    id          = Column(Integer, primary_key=True, index=True)
    medicine_id = Column(Integer, ForeignKey("medicines.id"), nullable=False)
    supplier    = Column(String(200))
    quantity    = Column(Integer)
    unit_cost   = Column(Float)
    total_cost  = Column(Float)
    status      = Column(String(20), default="pending")  # pending, ordered, received
    ordered_at  = Column(DateTime(timezone=True))
    received_at = Column(DateTime(timezone=True))
    created_at  = Column(DateTime(timezone=True), server_default=func.now())

    medicine = relationship("Medicine", back_populates="restock_orders")


# ── Sales Analytics ───────────────────────────────────────────
class SalesRecord(Base):
    __tablename__ = "sales_records"

    id          = Column(Integer, primary_key=True, index=True)
    date        = Column(Date, nullable=False, index=True)
    branch_id   = Column(Integer, ForeignKey("branches.id"))
    category    = Column(String(100))
    revenue     = Column(Float, default=0.0)
    orders_count = Column(Integer, default=0)
    units_sold   = Column(Integer, default=0)
    created_at   = Column(DateTime(timezone=True), server_default=func.now())
