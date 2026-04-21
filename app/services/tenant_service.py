from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.models.user_model import User
from ..models.tenant_model import Tenant
from core.database import SessionLocal
from fastapi.encoders import jsonable_encoder
from app.utils.enum import userType
from app.utils.pagination import PaginationRsponse
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
    def getList(find=None, option= {"page": 1, "limit": 10}) :
        db: Session = SessionLocal()
        try:
            result = (
                db.query(Tenant,User)   #  select both tables
                .join(User, Tenant.user_id == User.id)   #  JOIN condition
                .filter(Tenant.isDeleted == False)
                .order_by(desc(Tenant.created_at))
                .all()
            )

            # Convert into clean JSON format
            data = []
            for tenant, user in result:
                data.append({
                    "tenant": jsonable_encoder(tenant),
                    "user": {
                        "id": user.id,
                        "phone_number": user.phone_number
                    }
                })

            return PaginationRsponse.returnData(data,option)
        except Exception as e:
            print(e)




TenatService = tenantService()
