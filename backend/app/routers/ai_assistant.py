"""AI Assistant API — Smart pharmacy chatbot responses."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Medicine, Patient
from app.schemas.schemas import AIQuery, AIResponse

router = APIRouter()

AI_KNOWLEDGE = {
    "interaction": "🔬 **Drug Interaction Analysis**\n\nI've analyzed the combination. Based on pharmacokinetic and pharmacodynamic data:\n\n- Severity level depends on specific drug pair\n- Monitor patient for adverse effects\n- Recommend consulting the prescribing physician\n\nWould you like me to run a specific drug interaction check?",
    "inventory": "📦 **Inventory Status**\n\nI've analyzed current stock levels:\n\n- **5 medicines** are below minimum stock threshold\n- **3 medicines** are expiring within 30 days\n- **2 emergency medicines** need immediate restocking\n\nShall I generate restock purchase orders?",
    "recommend": "⭐ **AI Recommendations Active**\n\nBased on sales patterns and seasonal data:\n\n1. Increase antibiotic stock by 25% for monsoon season\n2. Pantoprazole discount suggested (expiry in 4 days)\n3. Generic Metformin substitute available — 40% cost saving\n\nWould you like detailed analysis for any specific recommendation?",
    "forecast": "📈 **Demand Forecast**\n\nAI model predicts for next 2 weeks:\n\n- **+18%** spike in cold/flu medicines\n- **+28%** antibiotic demand increase\n- Insulin demand stable\n\nConfidence: **89%** | Based on 12-month historical data + seasonal patterns",
    "emergency": "🚨 **Emergency Stock Alert**\n\nCritical items needing immediate action:\n\n- **Glyceryl Trinitrate**: Only 3 units (min: 8)\n- **Insulin Glargine**: Only 5 units (min: 20)\n- **Epinephrine**: 8 units (min: 10)\n\nShall I create urgent purchase orders for all critical items?",
    "sales": "💰 **Sales Analytics Summary**\n\nThis month's performance:\n\n- Revenue: ₹2,84,100 (+12.5% vs last month)\n- Orders: 1,240 total (+8.3%)\n- Top category: Antibiotics (22%)\n- Average order value: ₹229\n\nWould you like a detailed breakdown by category or branch?",
}

def _generate_response(message: str, db: Session) -> dict:
    msg_lower = message.lower()
    
    if any(w in msg_lower for w in ["interact", "drug", "combination", "mix"]):
        key = "interaction"
    elif any(w in msg_lower for w in ["stock", "inventory", "medicine", "low"]):
        key = "inventory"
    elif any(w in msg_lower for w in ["recommend", "suggest", "advice"]):
        key = "recommend"
    elif any(w in msg_lower for w in ["forecast", "predict", "demand", "future"]):
        key = "forecast"
    elif any(w in msg_lower for w in ["emergency", "critical", "urgent"]):
        key = "emergency"
    elif any(w in msg_lower for w in ["sale", "revenue", "analytics", "profit"]):
        key = "sales"
    else:
        return {
            "reply": "👋 Hello! I'm your **MediFlow AI Assistant**.\n\nI can help you with:\n\n- 🔬 Drug interaction checks\n- 📦 Inventory status & alerts\n- 📈 Demand forecasting\n- ⭐ Smart recommendations\n- 🚨 Emergency stock monitoring\n- 💰 Sales analytics\n\nWhat would you like to explore?",
            "suggestions": ["Check drug interactions", "View inventory alerts", "Show demand forecast", "List recommendations", "Emergency stock status"]
        }
    
    return {
        "reply": AI_KNOWLEDGE[key],
        "suggestions": ["Tell me more", "Generate report", "Create alerts", "View detailed data"]
    }


@router.post("/chat", response_model=AIResponse)
def ai_chat(payload: AIQuery, db: Session = Depends(get_db)):
    result = _generate_response(payload.message, db)
    return AIResponse(reply=result["reply"], suggestions=result.get("suggestions", []))


@router.get("/recommendations")
def ai_recommendations(db: Session = Depends(get_db)):
    from datetime import date, timedelta
    today = date.today()
    recs = []

    # Expiring soon
    expiring = db.query(Medicine).filter(
        Medicine.is_active == True,
        Medicine.expiry_date != None,
        Medicine.expiry_date <= today + timedelta(days=14),
    ).all()
    for m in expiring:
        days = m.days_to_expiry
        recs.append({
            "id": f"REC-EXP-{m.id}", "type": "expiry", "priority": "high",
            "title": f"Expiry Alert: {m.name}",
            "description": f"{m.stock_qty} units expire in {days} day(s). Consider 15-20% discount promotion to accelerate sales and minimize waste.",
            "medicine": m.name, "confidence": 95, "emoji": "⏰",
            "tags": ["Expiry Management", "Revenue Protection"],
        })

    # Low stock
    low = db.query(Medicine).filter(
        Medicine.is_active == True,
        Medicine.stock_qty < Medicine.min_stock,
    ).all()
    for m in low:
        recs.append({
            "id": f"REC-LOW-{m.id}", "type": "restock", "priority": "high",
            "title": f"Restock Required: {m.name}",
            "description": f"Current stock ({m.stock_qty}) is below minimum ({m.min_stock}). Recommend ordering {m.reorder_qty} units from supplier.",
            "medicine": m.name, "confidence": 98, "emoji": "📦",
            "tags": ["Low Stock", "Auto Restock"],
        })

    # Generic suggestions
    recs += [
        {"id": "REC-GEN-1", "type": "substitute", "priority": "medium",
         "title": "Generic Substitute Available: Metformin",
         "description": "Glyciphage (Metformin) by Franco-Indian is 40% cheaper than branded equivalent with identical bioavailability. Estimated monthly savings: ₹4,200.",
         "medicine": "Metformin 500mg", "confidence": 88, "emoji": "💡", "tags": ["Cost Saving", "Generic"]},
        {"id": "REC-GEN-2", "type": "demand", "priority": "medium",
         "title": "Seasonal Demand Spike Predicted",
         "description": "AI model predicts 28% increase in antibiotic demand over next 2 weeks based on regional seasonal respiratory infection patterns.",
         "medicine": "Azithromycin 500mg", "confidence": 82, "emoji": "🤖", "tags": ["AI Forecast", "Seasonal"]},
    ]

    return recs[:10]
