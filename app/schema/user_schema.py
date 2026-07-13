"""
ORM model = the actual DB table definition.
This is INTERNAL to the app — never return this directly from an API;
always convert to a DTO first.
"""
from sqlalchemy import Column, Integer, String, DateTime, func

from app.database.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    is_active = Column(Integer, default=1, nullable=False)
    created_at = Column(DateTime, server_default=func.now())