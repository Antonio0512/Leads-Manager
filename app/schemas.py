from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str
    confirm_password: str


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
    date_created: Optional[datetime] = None
    date_last_updated: Optional[datetime] = None


class LeadCreate(LeadBase):
    pass


class LeadUpdate(LeadBase):
    pass


class Lead(LeadBase):
    id: int

    class Config:
        from_attributes = True


class LeadError(BaseModel):
    error: dict


class TokenResponse(BaseModel):
    access_token: str
    user: dict


class TokenError(BaseModel):
    error: dict
