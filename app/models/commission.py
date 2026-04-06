




from enum import Enum

from sqlalchemy import Column, Float, ForeignKey, Integer, String,Enum

from app.models.base_models import BaseMixin
from core.database import Base
from app.utils.enum import bussinesType


class commission(Base, BaseMixin):
    __tablename__ = "commissions"

    id = Column(Integer, primary_key=True, index=True)
    bussinesType  = Column(Enum(bussinesType))  # "call" / "message"
    discount_percentage =Column(Integer)
    description = Column(String)        