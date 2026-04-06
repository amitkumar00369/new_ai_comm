

from sqlalchemy import Column, Integer, ForeignKey, String, String,Enum
from sqlalchemy.orm import relationship
from app.models import plan
from app.models.base_models import BaseMixin
from core.database import Base
from app.utils.enum import paymentStatus,paymentMethod,userType


class Payment(Base, BaseMixin):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True)
    paymentId = Column(String, unique=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Integer,default=0)
    currency = Column(String,default="USD")
    status = Column(Enum(paymentStatus), unique=True,default=paymentStatus.pending)  # "pending" / "completed" / "failed"
    transaction_id = Column(String, unique=True)
    payment_method = Column(Enum(paymentMethod),unique=True,default=paymentMethod.card)  # "card" / "upi" / "netbanking"
    userType = Column(Enum(userType),unique=True,default=userType.user)  # "admin" / "user"
    tenant = relationship("Tenant", back_populates="payments")
    user = relationship("User", back_populates="payments")  
    plan_id = Column(Integer, ForeignKey("plans.id"))
    plan = relationship("Plan", back_populates="payments")
    subscription_id = Column(Integer, ForeignKey("subscriptions.id"))
    subscription = relationship("Subscription", back_populates="payments")
    