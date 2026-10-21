"""Pydantic schemas for request/response validation."""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import date, datetime


# ── Medicine Schemas ──────────────────────────────────────────
class MedicineBase(BaseModel):
    name: str
    generic_name: Optional[str] = None
    category: str
    manufacturer: Optional[str] = None
    hsn_code: Optional[str] = None
    location: Optional[str] = None
    unit: str = "tablet"
    mrp: float
    cost_price: Optional[float] = None
    discount_pct: float = 0.0
    stock_qty: int = 0
    min_stock: int = 50
    max_stock: int = 500
    reorder_qty: int = 200
    expiry_date: Optional[date] = None
    mfg_date: Optional[date] = None
    requires_prescription: bool = False
    is_refrigerated: bool = False
    is_controlled: bool = False
    is_emergency: bool = False

class MedicineCreate(MedicineBase):
    pass

class MedicineUpdate(BaseModel):
    name: Optional[str] = None
    stock_qty: Optional[int] = None
    mrp: Optional[float] = None
    expiry_date: Optional[date] = None
    location: Optional[str] = None
    is_active: Optional[bool] = None

class MedicineResponse(MedicineBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    code: str
    is_active: bool
    created_at: Optional[datetime] = None
    stock_status: Optional[str] = None
    days_to_expiry: Optional[int] = None
    margin_pct: Optional[float] = None


# ── Patient Schemas ────────────────────────────────────────────
class PatientBase(BaseModel):
    name: str
    age: Optional[int] = None
    gender: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    blood_group: Optional[str] = None
    address: Optional[str] = None
    conditions: Optional[str] = None
    allergies: Optional[str] = None

class PatientCreate(PatientBase):
    pass

class PatientResponse(PatientBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    patient_code: str
    is_active: bool
    created_at: Optional[datetime] = None


# ── Prescription Schemas ───────────────────────────────────────
class PrescriptionItemCreate(BaseModel):
    medicine_id: int
    dosage: Optional[str] = None
    duration_days: Optional[int] = None
    instructions: Optional[str] = None
    quantity: Optional[int] = None

class PrescriptionItemResponse(PrescriptionItemCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    medicine: Optional[MedicineResponse] = None

class PrescriptionCreate(BaseModel):
    patient_id: int
    doctor_name: Optional[str] = None
    doctor_reg: Optional[str] = None
    hospital: Optional[str] = None
    notes: Optional[str] = None
    prescribed_date: Optional[date] = None
    items: List[PrescriptionItemCreate] = []

class PrescriptionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    rx_number: str
    patient_id: int
    doctor_name: Optional[str] = None
    hospital: Optional[str] = None
    status: str
    prescribed_date: Optional[date] = None
    dispensed_date: Optional[date] = None
    created_at: Optional[datetime] = None
    patient: Optional[PatientResponse] = None
    items: List[PrescriptionItemResponse] = []


# ── Order Schemas ──────────────────────────────────────────────
class OrderItemCreate(BaseModel):
    medicine_id: int
    quantity: int
    unit_price: float
    discount: float = 0.0

class OrderCreate(BaseModel):
    patient_id: int
    branch_id: Optional[int] = None
    order_type: str = "delivery"
    payment_method: str = "cash"
    notes: Optional[str] = None
    delivery_address: Optional[str] = None
    items: List[OrderItemCreate] = []

class OrderItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    medicine_id: int
    quantity: int
    unit_price: float
    discount: float
    total: float
    medicine: Optional[MedicineResponse] = None

class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    order_number: str
    patient_id: int
    status: str
    order_type: str
    subtotal: float
    discount: float
    tax: float
    total: float
    payment_method: str
    is_paid: bool
    created_at: Optional[datetime] = None
    patient: Optional[PatientResponse] = None
    items: List[OrderItemResponse] = []


# ── Branch Schemas ─────────────────────────────────────────────
class BranchResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    branch_code: str
    name: str
    location: Optional[str] = None
    manager: Optional[str] = None
    phone: Optional[str] = None
    is_main: bool
    status: str
    monthly_revenue: float
    staff_count: int


# ── Interaction Schemas ────────────────────────────────────────
class InteractionCheckRequest(BaseModel):
    drug1: str = Field(..., example="Metformin")
    drug2: str = Field(..., example="Alcohol")

class InteractionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    drug1: str
    drug2: str
    severity: str
    description: Optional[str] = None
    recommendation: Optional[str] = None
    mechanism: Optional[str] = None


# ── Reminder Schemas ───────────────────────────────────────────
class ReminderCreate(BaseModel):
    patient_id: int
    medicine_name: str
    reminder_time: str
    frequency: str = "daily"
    message_template: Optional[str] = None

class ReminderResponse(ReminderCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    is_active: bool
    last_sent: Optional[datetime] = None
    patient: Optional[PatientResponse] = None


# ── Delivery Schemas ───────────────────────────────────────────
class DeliveryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    order_id: int
    delivery_agent: Optional[str] = None
    agent_phone: Optional[str] = None
    status: str
    current_step: int
    estimated_mins: Optional[int] = None
    created_at: Optional[datetime] = None
    order: Optional[OrderResponse] = None


# ── Analytics Schemas ──────────────────────────────────────────
class DashboardStats(BaseModel):
    total_medicines: int
    total_patients: int
    today_orders: int
    today_revenue: float
    low_stock_count: int
    expiring_soon_count: int
    pending_prescriptions: int
    active_deliveries: int

class SalesTrend(BaseModel):
    labels: List[str]
    revenue: List[float]
    orders: List[int]


# ── AI Assistant ───────────────────────────────────────────────
class AIQuery(BaseModel):
    message: str = Field(..., example="Check interaction between Warfarin and Aspirin")
    context: Optional[str] = None

class AIResponse(BaseModel):
    reply: str
    suggestions: List[str] = []
    data: Optional[dict] = None


# ── Forecast Schemas ───────────────────────────────────────────
class ForecastResponse(BaseModel):
    labels: List[str]
    actual: List[Optional[float]]
    predicted: List[float]
    lower_bound: List[float]
    upper_bound: List[float]
    confidence: float
    trend: str
