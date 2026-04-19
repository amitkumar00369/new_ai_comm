from sqlalchemy import Column, DateTime, Integer,Boolean
from datetime import datetime

class BaseMixin:
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    isDeleted = Column(Boolean, default=False) 
    isBlocked = Column(Boolean, default=False) 