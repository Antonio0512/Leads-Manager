from typing import Union, Dict

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas
from app.config import get_db
from app.router.user_router import get_current_user
from app.crud import lead_crud

lead_router = APIRouter()


@lead_router.post("/leads/", response_model=Union[Dict[str, schemas.Lead], schemas.LeadError])
def create_lead(
        lead_data: schemas.LeadCreate,
        db: Session = Depends(get_db),
        current_user: schemas.User = Depends(get_current_user)
):
    try:
        lead = lead_crud.create_lead(db, lead_data, current_user)
        lead_dict = {
            "id": lead.id,
            "first_name": lead.first_name,
            "last_name": lead.last_name,
            "email": lead.email,
            "company": lead.company,
            "note": lead.note,
            "date_created": lead.date_created,
            "date_last_updated": lead.date_last_updated
        }
        return {"lead": lead_dict}
    except HTTPException as e:
        return schemas.LeadError(error={"status_code": e.status_code, "error_description": e.detail})
