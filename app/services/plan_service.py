from sqlalchemy.orm import Session
from ..models.plan import Plan
from core.database import SessionLocal
from fastapi.encoders import jsonable_encoder
from app.utils.enum import userType

class planService:
    
    @staticmethod
    def create(payload: dict):
        db: Session = SessionLocal()
        try: 
            newRecord = Plan(**payload)
            db.add(newRecord)
            db.commit()
            db.refresh(newRecord)
            return jsonable_encoder(newRecord)
        except Exception as e:
            db.rollback()
            raise
        finally:
            db.close()
    
    