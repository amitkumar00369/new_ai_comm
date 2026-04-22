import stat

from sqlalchemy import desc
from sqlalchemy.orm import Session


from app.models.tenant_model import Tenant
from app.utils.pagination import PaginationRsponse
# from stripe import PlanService
from ..models.agentModel import Agents
from ..models.plan import Plan

from core.database import SessionLocal
from fastapi.encoders import jsonable_encoder
from app.utils.enum import userType
from app.models.user_model import User
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
    def findByNumberWithUserDetails(number: str):
        db: Session = SessionLocal()
        try:
            agent = (
                db.query(Agents, User, Tenant)
                .join(User, Agents.assignedBy == User.id)
                .join(Tenant, User.id == Tenant.user_id)  #  Tenant join
                .filter(
                    Agents.agentWhatsappNumber == number,
                    Agents.isDeleted == False
                )
                .first()
            )

            if agent:
                agent_data, user_data, tenant_data = agent

                return jsonable_encoder({
                    "agent": agent_data,
                    "user": user_data,
                    "tenant": tenant_data
                })

            return None

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
    def getList(find: None, option= {"page": 1, "limit": 10}):
        db: Session = SessionLocal()
        try:
            agents = (db.query(Agents,Plan, User).join(Plan, Agents.plan_id==Plan.id).outerjoin(User, Agents.assignedBy == User.id).filter(Agents.isDeleted==False).order_by(desc(Agents.created_at))).all()
            data = []
            print("agenst",agents)
            for agent, plan, user in agents:   # 3 values unpack karo
                if user is None:
                    data.append({
                    "agent": jsonable_encoder(agent),
                    "plan": jsonable_encoder(plan),
                    "assignedBy": { }
                })
                else:
                    
                    
                    data.append({
                        "agent": jsonable_encoder(agent),
                        "plan": jsonable_encoder(plan),
                        "assignedBy": {
                            "id": user.id,
                            # "name": user.name,
                            "phone": user.phone_number
                        }
                    })
            return PaginationRsponse.returnData(data,option)
        except Exception as e:
            print(e)
    @staticmethod
    def getListByUser(find: None, option= {"page": 1, "limit": 10}):
        db: Session = SessionLocal()
        try:
            agents = (db.query(Agents,Plan).join(Plan, Agents.plan_id==Plan.id).filter(Agents.isDeleted==False,
                                              Agents.isBlocked==False,
                                              Agents.isAssigned==False).order_by(desc(Agents.created_at))).all()
            data = []
            for agent, plan in agents:
                data.append({
                    "agent": jsonable_encoder(agent),
                    "plan": jsonable_encoder(plan)
                })
            return PaginationRsponse.returnData(data,option)
        except Exception as e:
            print(e)
    

AgentService = agentService()