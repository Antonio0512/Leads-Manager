import bcrypt

from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.config import manager
from app.models import User
from app.schemas import UserCreate, UserUpdate, User as UserSchema


def register_user(
        user_data: UserCreate,
        db: Session
):
    if not user_data:
        raise HTTPException(status_code=400, detail="User data is empty")

    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="Email is already in use")

    if user_data.password != user_data.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

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
        email: str,
        password: str,
        db: Session,
):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=400, detail="Email does not exist")

    if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Invalid password")

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
        user_id,
        db: Session
):
    return _get_user_by_id(user_id, db)


def update_user(
        user_id: int,
        current_user: UserSchema,
        updated_data: UserUpdate,
        db: Session
):
    target_user = _get_user_by_id(user_id, db)

    if current_user.id != target_user.id:
        raise HTTPException(status_code=403, detail="You are not authorized!")

    new_email = updated_data.email
    if new_email and new_email != target_user.email:
        existing_user = _get_user_by_email(new_email, db)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already exists")

    for field, value in updated_data.model_dump().items():
        setattr(target_user, field, value)

    db.commit()
    db.refresh(target_user)

    return target_user


def delete_user(
        user_id: int,
        current_user: User,
        db: Session
):
    target_user = _get_user_by_id(user_id, db)

    if target_user.id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not authorized!")

    db.delete(target_user)
    db.commit()


def _get_user_by_email(email: str, db: Session):
    return db.query(User).filter(User.email == email).first()


def _get_user_by_id(
        user_id: int,
        db: Session,
):
    if user_id < 0:
        raise HTTPException(status_code=400, detail="User ID must be a positive number")

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
