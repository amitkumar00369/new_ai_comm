from enum import Enum

from sqlalchemy import Column, Integer, String, ForeignKey,Enum
from sqlalchemy.orm import relationship

from app.models.base_models import BaseMixin
from app.utils.enum import souceType
from core.database import Base

class Conversation(Base, BaseMixin):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    conversationId = Column(String, unique=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"))

    customer_phone = Column(String, index=True)
    source = Column(Enum(souceType),unique=True)  # "whatsapp" / "call"

    # tenant = relationship("Tenant", back_populates="conversations")
    # messages = relationship("Message", back_populates="conversation")