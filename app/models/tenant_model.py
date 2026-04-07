
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.models import payment
from app.models.base_models import BaseMixin
from core.database import Base

class Tenant(Base, BaseMixin):
    __tablename__ = "tenants"
    id = Column(Integer, primary_key=True, index=True)
    tenantId = Column(String, unique=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"),nullable=False)
    business_name = Column(String, nullable=False)
    plan_id = Column(Integer, ForeignKey("plans.id"))
    subscription_id = Column(Integer, ForeignKey("subscriptions.id"))
    # users = relationship("User", back_populates="tenant")
    # conversations = relationship("Conversation", back_populates="tenant")
    # leads = relationship("Lead", back_populates="tenant")
    # call_logs = relationship("CallLog", back_populates="tenant")
    # users= relationship("User", back_populates="tenant")
    # subscription = relationship("Subscription", back_populates="tenant", uselist=False)
    # payments = relationship("Payment", back_populates="tenant")