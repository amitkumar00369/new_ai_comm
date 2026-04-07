from sqlalchemy import ForeignKey, Interval, Table, Column, Integer, String, DateTime,Enum
from app.models.base_models import BaseMixin
from core.database import Base
from ..utils.enum import userType
from datetime import datetime


class sessionModel(Base,BaseMixin):
    __tablename__ = 'session'
    id = Column(Integer, primary_key=True)
    userId = Column(Integer, ForeignKey("users.id"))
    userType= Column(Enum(userType),  default=userType.user)
    email = Column(String, default="")
    phone_number =  Column(String, default="")
    createdAt = Column(DateTime, default=datetime.utcnow)  # auto insert
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # auto update
    accessToken = Column(String, default="")
    refreshToken = Column(String, default="")
    deviceId = Column(String, default="")
    deviceToken = Column(String, default="")
    deviceTypeId = Column(String, default="")