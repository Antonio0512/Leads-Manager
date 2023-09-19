from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import User, Lead
from app.schemas import UserCreate, UserUpdate
import bcrypt


def create_user(db: Session, user_data: UserCreate):
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

    return user


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def create_lead(db: Session, lead_data: dict):
    lead = Lead(**lead_data)
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return lead


def get_user_by_id(db: Session, user_id: int):
    if user_id < 0:
        raise HTTPException(status_code=400, detail="User ID must be a positive number")

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_lead_by_id(db: Session, lead_id: int):
    return db.query(Lead).filter(Lead.id == lead_id).first()


def get_leads(db: Session, skip: int = 0, limit: int = 10000):
    return db.query(Lead).offset(skip).limit(limit).all()


def update_user(db: Session, user: User, updated_data: UserUpdate):
    new_email = updated_data.email

    if new_email and new_email != user.email:
        existing_user = db.query(User).filter(User.email == new_email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already exists")

    for field, value in updated_data.model_dump().items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)

    return user


def update_lead(db: Session, lead: Lead, updated_data: dict):
    for key, value in updated_data.items():
        setattr(lead, key, value)
    db.commit()
    db.refresh(lead)
    return lead


def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return True
    return False


def delete_lead(db: Session, lead_id: int):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if lead:
        db.delete(lead)
        db.commit()
        return True
    return False
