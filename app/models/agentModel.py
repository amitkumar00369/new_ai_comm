from sqlalchemy import Column, ForeignKey, Integer, String,Boolean
from sqlalchemy.orm import relationship
from app.models import payment
from app.models.base_models import BaseMixin
from core.database import Base

class Agents(Base,BaseMixin):
    __tablename__ = "agents"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    agentId = Column(String)
    agentWhatsappNumber = Column(String, unique=True)
    countryCode = Column(String)
    isAssigned = Column(Boolean,default=False)
    assignedBy = Column(Integer, ForeignKey("users.id"))
    plan_id = Column(Integer, ForeignKey("plans.id"))
    