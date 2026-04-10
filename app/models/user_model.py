from numbers import Number

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum,ForeignKey
from app.models.base_models import BaseMixin
from core.database import Base
from datetime import datetime
from sqlalchemy.orm import relationship
from ..utils.enum import userType

class User(Base,BaseMixin):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    userId = Column(String, unique=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"),nullable=True)
    firstName = Column(String,nullable=True)
    lastName = Column(String, nullable=True)
    username=Column(String, nullable=True, unique=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    phone_number = Column(String, nullable=True)
    country_code = Column(String, nullable=True,default="+971")
    isEmailVerified = Column(Boolean, default=False)
    emailExpireAt = Column(DateTime,nullable=True)
    isPhoneVerified = Column(Boolean, default=False)
    phoneVerify = Column(Boolean, default=False)
    emailVerify = Column(Boolean, default=False)
    phoneExpireAt = Column(DateTime,nullable=True)
    phoneOtp = Column(Integer,nullable=True, default=23456)
    emailOtp = Column(Integer,nullable=True,default=123456)
    isProfileComplete = Column(Boolean, default=False)
    description = Column(String, nullable=True)
    is_active = Column(Boolean, default=False)
    userType= Column(Enum(userType),default=userType.user,nullable=True)
    image=Column(String, nullable=True)
    stripe_customer_id = Column(String, nullable=True)
    stripe_account_id = Column(String, nullable=True)
    dob = Column(DateTime,nullable=True)
    
    # tenant = relationship("Tenant", back_populates="users")
    plan_id = Column(Integer, ForeignKey("plans.id"),nullable=True)
    subscription_id = Column(Integer, ForeignKey("subscriptions.id"),nullable=True)
    refreshToken = Column(String, nullable=True)
    
    

