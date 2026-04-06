from sqlalchemy import Column, DateTime, Integer, false
from datetime import datetime

class BaseMixin:
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    isDeleted = Column(Integer, default=false) 
    isBlocked = Column(Integer, default=false) 