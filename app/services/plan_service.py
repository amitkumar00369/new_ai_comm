import stat

from fastapi.concurrency import run_in_threadpool
from sqlalchemy import desc
from sqlalchemy.orm import Session
from stripe import PlanService

from app.utils.pagination import PaginationRsponse
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
            
    @staticmethod
    def planUpgrade(id,payload):
        db: Session=SessionLocal()
        try:
            plan = db.query(Plan).filter(Plan.id==id,
                                         Plan.isDeleted==False).first()
            for key,value in payload.items():
                setattr(plan,key,value)
            db.commit()
            db.refresh(plan)
            return jsonable_encoder(plan)
        except Exception as e:
            db.rollback()
            raise
        finally:
            db.close()
            
            
    @staticmethod
    def findById(id: int):
        db: Session = SessionLocal()
        try:
            plan = db.query(Plan).filter(Plan.id==id).first()
            return jsonable_encoder(plan)
        except Exception as e:
            db.rollback()
            raise
        finally:
            db.close()
    @staticmethod
    def findByName(name: str):
        db: Session = SessionLocal()
        try:
            plan = db.query(Plan).filter(Plan.name==name,
                                         Plan.isDeleted==False).first()
            return jsonable_encoder(plan)
        except Exception as e:
            db.rollback()
            raise
        finally:
            db.close()
    
    
    @staticmethod
    def getList(find=None, option = {"page": 1,"limit": 10}):
        db: Session = SessionLocal()
        try:
            plans = (db.query(Plan).filter(Plan.isDeleted==False).order_by(desc(Plan.created_at))).all()
            data= jsonable_encoder(plans)
            return PaginationRsponse.returnData(data, option)
        
        
        except Exception as e:
            print(e)
    
PlanService = planService()