from sqlalchemy import Column, Integer, String, Float,Enum

from app.models.base_models import BaseMixin
from core.database import Base
from app.utils.enum import periodType,planType

class Plan(Base, BaseMixin):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, index=True)
    planId = Column(String, unique=True, index=True)
    name = Column(String)  
    planCode = Column(String,unique=True)
    planType = Column(Enum(planType), default=planType.free)  # "free" / "paid"
    price = Column(Float ,default=0.0)
    period = Column(Enum(periodType), default=periodType.default)  # monthly / yearly
    max_requests = Column(Integer,default=0)     # AI usage limit
    max_calls = Column(Integer,default=0)        # call limit
    max_messages = Column(Integer,default=0)     # WhatsApp limit