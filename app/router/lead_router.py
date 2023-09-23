from fastapi import APIRouter, Depends, HTTPException, Query

from sqlalchemy.orm import Session

from typing import Union, Dict, List

from app import schemas
from app.config import get_db
from app.router.user_router import get_current_user
from app.crud import lead_crud

lead_router = APIRouter()


@lead_router.post("/leads", response_model=Union[Dict[str, schemas.Lead], schemas.LeadError])
def create_lead(
        lead_data: schemas.LeadCreate,
        current_user: schemas.User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    try:
        lead = lead_crud.create_lead(lead_data, current_user, db)
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


@lead_router.get("/leads", response_model=List[schemas.Lead])
def get_all_leads(
        db: Session = Depends(get_db),
        skip: int = Query(0, alias="skip"),
        limit: int = Query(100, alias="limit")
):
    return lead_crud.get_all_leads(db, skip, limit)


@lead_router.get("/leads/{lead_id}", response_model=schemas.Lead)
def get_lead(
        lead_id: int,
        current_user: schemas.User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    # noinspection PyUnusedLocal
    return lead_crud.get_one_lead(lead_id, current_user, db)


@lead_router.put("/leads/{lead_id}/update", response_model=schemas.Lead)
def update_lead(
        lead_id: int,
        update_data: schemas.LeadUpdate,
        current_user: schemas.User = Depends(get_current_user),
        db: Session = Depends(get_db),
):
    return lead_crud.update_lead(lead_id, update_data, current_user, db)


@lead_router.delete("/leads/{lead_id}/delete", response_model=Dict)
def delete_lead(
        lead_id: int,
        current_user: schemas.User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    lead_crud.delete_lead(lead_id, current_user, db)
    return {"message": "Lead deleted successfully"}
