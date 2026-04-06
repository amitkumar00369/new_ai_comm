from sqlalchemy import Column, Integer, String, Text, ForeignKey

from app.models.base_models import BaseMixin
from core.database import Base

class CallLog(Base, BaseMixin):
    __tablename__ = "call_logs"

    id = Column(Integer, primary_key=True, index=True)
    callId = Column(String, unique=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"))

    caller_number = Column(String)
    duration = Column(Integer)  # seconds
    transcript = Column(Text)
    source = Column(String)  # "inbound" / "outbound"