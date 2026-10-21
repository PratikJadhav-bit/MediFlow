"""Drug interaction checker API."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import Optional
from app.database import get_db
from app.models.models import DrugInteraction
from app.schemas.schemas import InteractionCheckRequest, InteractionResponse

router = APIRouter()


@router.post("/check", summary="Check drug-drug interaction")
def check_interaction(payload: InteractionCheckRequest, db: Session = Depends(get_db)):
    d1, d2 = payload.drug1.strip(), payload.drug2.strip()
    result = db.query(DrugInteraction).filter(
        or_(
            and_(DrugInteraction.drug1.ilike(f"%{d1}%"), DrugInteraction.drug2.ilike(f"%{d2}%")),
            and_(DrugInteraction.drug1.ilike(f"%{d2}%"), DrugInteraction.drug2.ilike(f"%{d1}%")),
        )
    ).first()

    if result:
        return {
            "found": True,
            "drug1": result.drug1, "drug2": result.drug2,
            "severity": result.severity,
            "description": result.description,
            "recommendation": result.recommendation,
            "mechanism": result.mechanism,
        }
    return {
        "found": False,
        "drug1": d1, "drug2": d2,
        "severity": "none",
        "description": "No known clinically significant interaction found between these drugs in our database.",
        "recommendation": "Continue with normal dosing. Always monitor for unexpected effects.",
        "mechanism": "No known pharmacokinetic or pharmacodynamic interaction mechanism documented.",
    }


@router.get("/all", response_model=list, summary="List all known interactions")
def list_interactions(db: Session = Depends(get_db)):
    interactions = db.query(DrugInteraction).all()
    return [
        {"id": i.id, "drug1": i.drug1, "drug2": i.drug2, "severity": i.severity,
         "description": i.description, "recommendation": i.recommendation}
        for i in interactions
    ]
