
from numbers import Number

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum,ForeignKey,JSON,UniqueConstraint
from app.models.base_models import BaseMixin
from core.database import Base
from datetime import datetime
from sqlalchemy.orm import relationship
from ..utils.enum import userType,bussinesType
class BussinessServiceModel(Base,BaseMixin):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String)
    price = Column(Integer)
    location = Column(String)
    meta_data = Column(JSON)
    __table_args__ = (
        UniqueConstraint("tenant_id", "title", name="uq_tenant_title"),
    )
   