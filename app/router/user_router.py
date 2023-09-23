import os
import jwt

from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from sqlalchemy.orm import Session

from typing import Union, Dict

from app import schemas
from app.crud import user_crud
from app.config import get_db
from app.models import User

user_router = APIRouter()

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

    except Exception:
        raise HTTPException(status_code=401, detail="Could not validate credentials")


@user_router.post("/users", response_model=Union[schemas.TokenResponse, schemas.TokenError])
def register_user(
        user_data: schemas.UserCreate,
        db: Session = Depends(get_db)
):
    try:
        data = user_crud.register_user(user_data, db)
        return schemas.TokenResponse(**data)
    except HTTPException as e:
        raise e


@user_router.post("/login", response_model=Union[schemas.TokenResponse, schemas.TokenError])
def login(
        data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    try:
        user_data = user_crud.login_user(data.username, data.password, db)
        return schemas.TokenResponse(**user_data)
    except HTTPException as e:
        raise e


@user_router.get("/users")
def get_users(
        db: Session = Depends(get_db),
        skip: int = Query(0, alias="skip"),
        limit: int = Query(100, alias="limit")
):
    return user_crud.get_users(db, skip, limit)


@user_router.get("/users/{id}")
def get_user(
        user_id: int,
        db: Session = Depends(get_db)
):
    return user_crud.get_one_user(user_id, db)


@user_router.put("users/{id}/update", response_model=schemas.User)
def update_user(
        user_id: int,
        updated_data: schemas.UserUpdate,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    return user_crud.update_user(user_id, current_user, updated_data, db)


@user_router.delete("/users/{id}/delete", response_model=Dict)
def delete_user(
        user_id: int,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
):
    user_crud.delete_user(user_id, current_user, db)
    return {"message": "User deleted successfully"}
