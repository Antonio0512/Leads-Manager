from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import Lead
from app.schemas import LeadCreate, User


def create_lead(
        db: Session,
        lead_data: LeadCreate,
        current_user: User
):
    required_fields = ['first_name', 'last_name', 'email', 'company']
    missing_fields = [field for field in required_fields if not getattr(lead_data, field, None)]

    if missing_fields:
        raise HTTPException(status_code=400, detail=f"Missing required fields: {', '.join(missing_fields)}")

    current_timestamp = datetime.utcnow()
    lead_data.date_created = current_timestamp
    lead_data.date_last_updated = current_timestamp

    if db.query(Lead).filter(Lead.email == lead_data.email).first():
        raise HTTPException(status_code=400, detail="Email already associated with another lead")

    lead = Lead(**lead_data.model_dump(), owner_id=current_user.id)
    db.add(lead)
    db.commit()
    db.refresh(lead)

    return lead


def get_lead_by_id(db: Session, lead_id: int):
    return db.query(Lead).filter(Lead.id == lead_id).first()


def get_leads(db: Session, skip: int = 0, limit: int = 10000):
    return db.query(Lead).offset(skip).limit(limit).all()


def update_lead(db: Session, lead: Lead, updated_data: dict):
    for key, value in updated_data.items():
        setattr(lead, key, value)
    db.commit()
    db.refresh(lead)
    return lead


def delete_lead(db: Session, lead_id: int):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if lead:
        db.delete(lead)
        db.commit()
        return True
    return False
