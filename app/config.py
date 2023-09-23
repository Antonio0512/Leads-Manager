import os
import jwt

from dotenv import load_dotenv

from datetime import timedelta, datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from fastapi_login import LoginManager

load_dotenv()

SECRET_KEY = os.environ.get("SECRET")
manager = LoginManager(SECRET_KEY, token_url='/login')

DATABASE_URL = os.environ.get("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=5)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
