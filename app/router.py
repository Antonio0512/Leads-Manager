from fastapi import APIRouter, Depends, Request, Query, HTTPException

from sqlalchemy.orm import Session

from app import schemas, crud
from app.config import get_db

router = APIRouter()


@router.post("/users/")
def create_user(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user_data)


@router.get("/users/")
def get_users(db: Session = Depends(get_db), skip: int = Query(0, alias="skip"),
              limit: int = Query(100, alias="limit")):
    return crud.get_users(db, skip, limit)


@router.get("/users/{id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    return crud.get_user_by_id(db, user_id)


@router.post("users/{id}/update")
def update_user(user_id: int, updated_data: schemas.UserUpdate, db: Session = Depends(get_db)):
    user = crud.get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")


    updated_user = crud.update_user(db, user, updated_data)

    if not updated_user:
        raise HTTPException(status_code=400, detail="User update failed")

    return updated_user
