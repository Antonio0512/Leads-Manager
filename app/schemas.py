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
    leads: List["Lead"] = []

    class Config:
        orm_mode = True


class LeadBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    company: str
    note: Optional[str] = None
    date_created: datetime
    date_last_updated: datetime

    class Config:
        arbitrary_types_allowed = True


class LeadCreate(LeadBase):
    pass


class Lead(LeadBase):
    id: int

    class Config:
        orm_mode = True
