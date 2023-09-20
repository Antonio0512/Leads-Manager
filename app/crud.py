from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.config import manager
from app.models import User, Lead
from app.schemas import UserCreate, UserUpdate
import bcrypt


def register_user(
        db: Session,
        user_data: UserCreate
):
    if not user_data:
        raise HTTPException(status_code=400, detail="User data is empty")

    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email is already in use")

    hashed_password = bcrypt.hashpw(user_data.password.encode('utf-8'), bcrypt.gensalt())

    user = User(email=user_data.email, password=hashed_password.decode('utf-8'))

    db.add(user)
    db.commit()
    db.refresh(user)

    access_token = manager.create_access_token(
        data={"sub": user.email}
    )

    response_data = {"access_token": access_token, "user": {"email": user_data.email}}

    return response_data


def login_user(
        db: Session,
        email: str,
        password: str
):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=400, detail="Email does not exist")

    if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        raise HTTPException(status_code=400, detail="Invalid password")

    access_token = manager.create_access_token(
        data={'sub': user.email}
    )

    response_data = {"access_token": access_token, "user": {"email": user.email}}

    return response_data


def get_users(
        db: Session,
        skip: int = 0,
        limit: int = 100
):
    return db.query(User).offset(skip).limit(limit).all()


def get_one_user(
        db: Session,
        user_id
):
    return _get_user_by_id(db, user_id)


def update_user(
        db: Session,
        user_id: int,
        current_user: User,
        updated_data: UserUpdate
):
    target_user = _get_user_by_id(db, user_id)
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")

    if current_user.id != target_user.id:
        raise HTTPException(status_code=403, detail="You are not authorized!")

    new_email = updated_data.email
    if new_email and new_email != target_user.email:
        existing_user = _get_user_by_email(db, new_email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already exists")

    for field, value in updated_data.model_dump().items():
        setattr(target_user, field, value)

    db.commit()
    db.refresh(target_user)

    return target_user


def delete_user(
        db: Session,
        user_id: int,
        current_user: User
):
    target_user = _get_user_by_id(db, user_id)
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")

    if target_user.id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not authorized!")

    db.delete(target_user)
    db.commit()


def create_lead(db: Session, lead_data: dict):
    lead = Lead(**lead_data)
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


def _get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def _get_user_by_id(
        db: Session,
        user_id: int
):
    if user_id < 0:
        raise HTTPException(status_code=400, detail="User ID must be a positive number")

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
