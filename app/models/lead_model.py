from enum import Enum

from sqlalchemy import Column, Integer, String, ForeignKey,Enum

from sqlalchemy.orm import relationship

from app.models.base_models import BaseMixin
from core.database import Base
from app.utils.enum import souceType

class Lead(Base, BaseMixin):
    __tablename__ = "leads"
    id = Column(Integer, primary_key=True, index=True)
    leadId = Column(String, unique=True, index=True)
    tenantId = Column(String, unique=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    
    serviceId = Column(Integer,ForeignKey("services.id"))
    name = Column(String)
    phone = Column(String)
    tenant_phone = Column(String)
    agent_number = Column(String)
    service = Column(String)
    source = Column(Enum(souceType),unique=True)  # "call" / "whatsapp"
    # tenant = relationship("Tenant", back_populates="leads")