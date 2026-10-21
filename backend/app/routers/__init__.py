"""AI Assistant, recommendations, and demand forecast."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date, timedelta
from app.database import get_db
from app.models.models import Medicine, Patient, Order
from app.schemas.schemas import AIQuery, AIResponse, ForecastResponse

router = APIRouter()

# Routers for AI assistant
from app.routers import ai_assistant, forecast

# Export both
__all__ = ["ai_assistant", "forecast"]
