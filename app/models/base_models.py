from sqlalchemy import Column, DateTime, Integer
from datetime import datetime

class BaseMixin:
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    isDeleted = Column(Integer, default=False) 
    isBlocked = Column(Integer, default=False) 