from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from app import schemas, crud
from app.config import get_db

router = APIRouter()


@router.post("/users/", response_model=schemas.TokenResponse)
def register_user(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.register_user(db, user_data)


@router.post("/login", response_model=schemas.TokenResponse)
def login(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return crud.login_user(db, data.username, data.password)

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


@router.post("/users/{id}/delete")
def delete_user(
        user_id: int,
        db: Session = Depends(get_db),
        current_user: schemas.User = Depends()
):
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Permission denied")

    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    crud.delete_user(db, user_id)

    return {"message": "User deleted successfully"}
