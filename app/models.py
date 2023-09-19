from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.config import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    leads = relationship("Lead", back_populates="owner")


class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, index=True)
    company = Column(String)
    note = Column(String)
    date_created = Column(DateTime)
    date_last_updated = Column(DateTime)

    owner = relationship("User", back_populates="leads")
