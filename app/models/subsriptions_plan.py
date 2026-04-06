from sqlalchemy import Column, Enum, Integer, ForeignKey, DateTime, String
from datetime import datetime, timedelta

from app.models.base_models import BaseMixin
from core.database import Base
from app.utils.enum import periodType, planStatus,planType


class Subscription(Base, BaseMixin):
    __tablename__ = "subscriptions"
    id = Column(Integer, primary_key=True, index=True)
    subscriptionsId = Column(String, unique=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"))
    planCode = Column(String, ForeignKey("plans.planCode"))
    plan_id = Column(Integer, ForeignKey("plans.id"))
    user_id  = Column(Integer, ForeignKey("users.id"))
    status = Column(Enum(planStatus), default=planStatus.active)  # active / expired
    planType = Column(Enum(planType), default=planType.free)  # "free" / "paid"
    period = Column(Enum(periodType), default=periodType.default)  # monthly / yearly
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime)
    used_requests = Column(Integer, default=0)
    used_calls = Column(Integer, default=0)
    used_messages = Column(Integer, default=0)