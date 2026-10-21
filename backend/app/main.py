"""
MediFlow AI — FastAPI Backend
Production-grade pharmacy management REST API
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time

from app.database import engine, Base
from app.routers import (
    medicines, patients, prescriptions, orders,
    analytics, branches, interactions, reminders,
    deliveries, emergency, ai_assistant, forecast
)
from app.seed_data import seed_database

# ── Create all DB tables ──────────────────────────────────────
Base.metadata.create_all(bind=engine)

# ── Seed DB with sample data ──────────────────────────────────
seed_database()

# ── FastAPI App ───────────────────────────────────────────────
app = FastAPI(
    title="MediFlow AI API",
    description="""
## 🏥 MediFlow AI — Pharmacy Management Platform

A production-grade REST API powering the next generation of smart pharmacies.

### Features
- 💊 **Medicine Inventory** — Full CRUD with stock tracking
- 📋 **Digital Prescriptions** — Rx management workflow
- 🤖 **AI Recommendations** — Smart inventory intelligence
- 📊 **Sales Analytics** — Revenue & demand insights
- 🚨 **Emergency Alerts** — Critical stock monitoring
- 🏪 **Multi-Branch** — Centralized branch management
- 💬 **AI Assistant** — Natural language pharmacy queries
    """,
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    contact={
        "name": "MediFlow AI Team",
        "email": "api@mediflow.ai",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# ── CORS ──────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Request Timing Middleware ─────────────────────────────────
@app.middleware("http")
async def add_process_time_header(request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    response.headers["X-Process-Time"] = f"{(time.perf_counter() - start)*1000:.2f}ms"
    return response

# ── Routers ───────────────────────────────────────────────────
app.include_router(medicines.router,     prefix="/api/v1/medicines",     tags=["💊 Medicines"])
app.include_router(patients.router,      prefix="/api/v1/patients",      tags=["👤 Patients"])
app.include_router(prescriptions.router, prefix="/api/v1/prescriptions", tags=["📋 Prescriptions"])
app.include_router(orders.router,        prefix="/api/v1/orders",        tags=["🛒 Orders"])
app.include_router(analytics.router,     prefix="/api/v1/analytics",     tags=["📊 Analytics"])
app.include_router(branches.router,      prefix="/api/v1/branches",      tags=["🏪 Branches"])
app.include_router(interactions.router,  prefix="/api/v1/interactions",  tags=["⚡ Drug Interactions"])
app.include_router(reminders.router,     prefix="/api/v1/reminders",     tags=["📱 Reminders"])
app.include_router(deliveries.router,    prefix="/api/v1/deliveries",    tags=["🚚 Deliveries"])
app.include_router(emergency.router,     prefix="/api/v1/emergency",     tags=["🚨 Emergency"])
app.include_router(ai_assistant.router,  prefix="/api/v1/ai",            tags=["🤖 AI Assistant"])
app.include_router(forecast.router,      prefix="/api/v1/forecast",      tags=["📈 Forecast"])

# ── Health Check ──────────────────────────────────────────────
@app.get("/", tags=["Health"])
async def root():
    return {
        "status": "✅ MediFlow AI API is running",
        "version": "2.0.0",
        "docs": "/docs",
        "environment": "development"
    }

@app.get("/health", tags=["Health"])
async def health_check():
    return JSONResponse({
        "status": "healthy",
        "api_version": "2.0.0",
        "database": "connected",
        "timestamp": time.time()
    })
