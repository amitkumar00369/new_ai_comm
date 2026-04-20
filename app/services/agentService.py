import stat

from sqlalchemy.orm import Session
# from stripe import PlanService
from ..models.agentModel import Agents
from core.database import SessionLocal
from fastapi.encoders import jsonable_encoder
from app.utils.enum import userType

class agentService:
    
    @staticmethod
    def create(payload: dict):
        db: Session = SessionLocal()
        try: 
            newRecord = Agents(**payload)
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
    def agentUpgrade(id,payload):
        db: Session=SessionLocal()
        try:
            plan = db.query(Agents).filter(Agents.id==id,
                                         Agents.isDeleted==False).first()
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
            agent = db.query(Agents).filter(Agents.id==id).first()
            return jsonable_encoder(agent)
        except Exception as e:
            db.rollback()
            raise
        finally:
            db.close()
    @staticmethod
    def findByNumber(number: str):
        db: Session = SessionLocal()
        try:
            agent = db.query(Agents).filter(Agents.agentWhatsappNumber==number,
                                         Agents.isDeleted==False).first()
            return jsonable_encoder(agent)
        except Exception as e:
            db.rollback()
            raise
        finally:
            db.close()
    @staticmethod
    def findByName(name: str):
        db: Session = SessionLocal()
        try:
            agent = db.query(Agents).filter(Agents.name==name,
                                         Agents.isDeleted==False).first()
            return jsonable_encoder(agent)
        except Exception as e:
            db.rollback()
            raise
        finally:
            db.close()
    
    
    @staticmethod
    def getList():
        db: Session = SessionLocal()
        try:
            agents = (db.query(Agents).filter(Agents.isDeleted==False).order_by(Agents.created_at)).all()
            return jsonable_encoder(agents)
        except Exception as e:
            print(e)

AgentService = agentService()