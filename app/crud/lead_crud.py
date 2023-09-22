from fastapi import HTTPException

from sqlalchemy.orm import Session

from datetime import datetime

from app.models import Lead
from app import schemas


def create_lead(
        lead_data: schemas.LeadCreate,
        current_user: schemas.User,
        db: Session
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


def get_all_leads(
        db: Session,
        skip: int = 0,
        limit: int = 10000
):
    return db.query(Lead).offset(skip).limit(limit).all()


# noinspection PyUnusedLocal
def get_one_lead(
        lead_id: int,
        current_user: schemas.User,
        db: Session
):
    return _get_lead_by_id(lead_id, db)


def update_lead(
        lead_id: int,
        updated_data: schemas.LeadUpdate,
        current_user: schemas.User,
        db: Session,
):
    target_lead = _get_lead_by_id(lead_id, db)

    if target_lead.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not authorized!")

    date_created = target_lead.date_created

    if db.query(Lead).filter(Lead.email == target_lead.email, Lead.id != lead_id).first():
        raise HTTPException(status_code=400, detail="Email already associated with another lead")

    updated_data.date_created = date_created
    updated_data.date_last_updated = datetime.utcnow()

    for field, value in updated_data.model_dump().items():
        setattr(target_lead, field, value)
    db.commit()
    db.refresh(target_lead)
    return target_lead


def delete_lead(
        lead_id: int,
        current_user: schemas.User,
        db: Session
):
    target_lead = _get_lead_by_id(lead_id, db)

    if target_lead.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not authorized!")

    db.delete(target_lead)
    db.commit()


def _get_lead_by_id(
        lead_id: int,
        db: Session
):
    if lead_id < 0:
        raise HTTPException(status_code=400, detail="User ID must be a positive number")

    lead = db.query(Lead).filter(Lead.id == lead_id).first()

    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    return lead
