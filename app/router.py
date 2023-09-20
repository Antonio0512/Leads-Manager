import os
from typing import Union

import jwt
from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app import schemas, crud
from app.config import get_db
from app.models import User

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login/")


def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db),
):
    try:
        payload = jwt.decode(token, os.environ.get("SECRET"), algorithms=["HS256"])
        email: str = payload.get("sub")

        if email is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")

        user = db.query(User).filter(User.email == email).first()
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")

        return user

    except Exception as e:
        print(f"Exception: {e}")
        raise HTTPException(status_code=401, detail="Could not validate credentials")


@router.post("/users/", response_model=Union[schemas.TokenResponse, schemas.TokenError])
def register_user(
        user_data: schemas.UserCreate,
        db: Session = Depends(get_db)
):
    try:
        user_data = crud.register_user(db, user_data)
        return schemas.TokenResponse(**user_data)
    except HTTPException as e:
        return schemas.TokenError(error={"status_code": e.status_code, "error_description": e.detail})


@router.post("/login/", response_model=Union[schemas.TokenResponse, schemas.TokenError])
def login(
        data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    try:
        user_data = crud.login_user(db, data.username, data.password)
        return schemas.TokenResponse(**user_data)
    except HTTPException as e:
        return schemas.TokenError(error={"status_code": e.status_code, "error_description": e.detail})


@router.get("/users/")
def get_users(
        db: Session = Depends(get_db),
        skip: int = Query(0, alias="skip"),
        limit: int = Query(100, alias="limit")
):
    return crud.get_users(db, skip, limit)


@router.get("/users/{id}")
def get_user(
        user_id: int,
        db: Session = Depends(get_db)
):
    return crud.get_one_user(db, user_id)


@router.put("users/{id}/update", response_model=schemas.User)
def update_user(
        user_id: int,
        updated_data: schemas.UserUpdate,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    return crud.update_user(db, user_id, current_user, updated_data)


@router.delete("/users/{id}/delete", response_model=None)
def delete_user(
        user_id: int,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
):
    crud.delete_user(db, user_id, current_user)
    return {"message": "User deleted successfully"}
