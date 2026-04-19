from sqlalchemy.orm import Session
from ..models.tenant_model import Tenant
from core.database import SessionLocal
from fastapi.encoders import jsonable_encoder
from app.utils.enum import userType

class tenantService:

    @staticmethod
    def createtenant(data: dict):
        db: Session = SessionLocal()
        try:
            new_record = Tenant(**data)
            db.add(new_record)
            db.commit()
            db.refresh(new_record)
            return jsonable_encoder(new_record)
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

    @staticmethod
    def gettenantBytenantid(tenantId: str):
        db: Session = SessionLocal()
        return jsonable_encoder(db.query(Tenant).filter(Tenant.tenantId == tenantId).first())

    @staticmethod
    def findByIdUpdate(id: int, payload: dict):
        db: Session = SessionLocal()
        tenat = db.query(Tenant).filter(Tenant.id == id and Tenant.isDeleted==False).first()
        if not tenat:
            return None  # or raise HTTPException

        for key, value in payload.items():
            setattr(tenat, key, value)

        db.commit()
        db.refresh(tenat)
        return jsonable_encoder(tenat)
    @staticmethod
    def findById(id: int):
        db: Session = SessionLocal()
        try:
            tenat = db.query(Tenant).filter(Tenant.id == id and Tenant.isDeleted==False).first()
            return jsonable_encoder(tenat)
        except Exception as e:
            print(e)
    @staticmethod
    def findByUserid(userId: str) :
        db: Session = SessionLocal()
        try:
            tenat = db.query(Tenant).filter(Tenant.user_id == userId and Tenant.isDeleted==False).first()
            return jsonable_encoder(tenat)
        except Exception as e:
            print(e)
    @staticmethod
    def getList() :
        db: Session = SessionLocal()
        try:
            tenat = (
            db.query(Tenant)
            .filter(Tenant.isDeleted == False and Tenant.userType!=userType.admin)
            .order_by(Tenant.created_at)   # ✅ correct
            .all()
        )
            return jsonable_encoder(tenat)
        except Exception as e:
            print(e)




TenatService = tenantService()
