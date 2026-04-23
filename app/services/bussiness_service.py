from sqlite3 import IntegrityError, OperationalError

from app.models.bussinessServiceModel import BussinessServiceModel
from sqlalchemy import desc, exists
from sqlalchemy.orm import Session

from app.models.lead_model import Lead
from app.utils.pagination import PaginationRsponse
from ..models.user_model import User
from core.database import SessionLocal
from fastapi.encoders import jsonable_encoder
from app.utils.enum import userType
from app.models.tenant_model import Tenant



class bussinessService:
    
    @staticmethod
    def create():
        pass
    
    @staticmethod
    def bulkCreate(data):
        db: Session = SessionLocal()

        try:
            if not data:
                return {
                    "status": False,
                    "message": "No data provided"
                }

            #  assume all items have same tenant_id
            tenant_id = data[0].get("tenant_id")

            # Step 1: fetch existing titles
            existing_titles = set(
                x[0] for x in db.query(BussinessServiceModel.title)
                .filter(BussinessServiceModel.tenant_id == tenant_id)
                .all()
            )

            valid = []
            duplicates = []

            # Step 2: split valid & duplicate
            for item in data:
                title = item.get("title")

                if not title:
                    continue  # skip invalid rows

                if title in existing_titles:
                    duplicates.append(item)
                else:
                    valid.append(item)

            # Step 3: bulk insert valid data
            if valid:
                db.bulk_insert_mappings(BussinessServiceModel, valid)
                db.commit()

            return {
                "status": True,
                "inserted_count": len(valid),
                "duplicate_count": len(duplicates),
                "duplicates": duplicates,
                "message": "Bulk upload completed"
            }

        except Exception as e:
            db.rollback()
            return {
                "status": False,
                "message": "Something went wrong",
                "error": str(e)
            }

        finally:
            db.close()
    @staticmethod
    def findByUserId(userId):
        db: Session = SessionLocal()
        try:
            services = (
            db.query(BussinessServiceModel)
            .filter(BussinessServiceModel.isDeleted == False,
                    BussinessServiceModel.user_id==userId,
                     ~exists().where(Lead.serviceId == BussinessServiceModel.id))
            .order_by(desc(BussinessServiceModel.created_at))   #  correct
            .all())
            return jsonable_encoder(services)
        except Exception as e:
            print(e)
        finally:
            db.close()
    @staticmethod
    def deleteById(id):
        db: Session = SessionLocal()
        try:
            service = (
                db.query(BussinessServiceModel)
                .filter(
                    BussinessServiceModel.id == id,
                    BussinessServiceModel.isDeleted == False
                )
                .first()
            )
            service.isDeleted = True

            db.commit()
            db.refresh(service)
            return jsonable_encoder(service)
        except Exception as e:
            print(e)
        finally:
            db.close()
    @staticmethod
    def deleteByUserId(id):
        db: Session = SessionLocal()
        try:
            services = (
                db.query(BussinessServiceModel)
                .filter(
                    BussinessServiceModel.user_id == id,
                    BussinessServiceModel.isDeleted == False
                )
                .all()
            )
            for service in services:
                service.isDeleted = True

            db.commit()
            return jsonable_encoder(services)
        except Exception as e:
            print(e)
        finally:
            db.close()
            
    @staticmethod
    def findById(id):
        db: Session = SessionLocal()
        try:
            service = db.query(BussinessServiceModel).filter(
                    BussinessServiceModel.id == id,
                    BussinessServiceModel.isDeleted == False
                ).first()
            return jsonable_encoder(service)
        except Exception as e:
            print(e)
        finally:
            db.close()
        
            
            
        
        
BussinessService = bussinessService()