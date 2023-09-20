from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    email: str


class User(UserBase):
    id: int
    leads: List = []

    class Config:
        from_attributes = True


class LeadBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    company: str
    note: Optional[str] = None
    date_created: datetime
    date_last_updated: datetime


class LeadCreate(LeadBase):
    pass


class LeadUpdate(LeadBase):
    pass


class Lead(LeadBase):
    id: int

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    user: dict


class TokenError(BaseModel):
    error: dict

