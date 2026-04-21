from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.utils.pagination import PaginationRsponse
from ..models.user_model import User
from core.database import SessionLocal
from fastapi.encoders import jsonable_encoder
from app.utils.enum import userType


class userService:

    @staticmethod
    def createUser(data: dict):
        db: Session = SessionLocal()
        try:
            new_record = User(**data)
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
    def getUser(phone_number):
        db: Session = SessionLocal()
        try:
            results = db.query(User).filter(User.phone_number == phone_number,
                                     User.isDeleted==False,
                                     User.phoneVerify==True).first()
            return jsonable_encoder(results)
        finally:
            db.close()
            
    @staticmethod
    def getUserByEmail(email: str):
        db: Session = SessionLocal()
        return jsonable_encoder(db.query(User).filter(User.email == email).first())

    @staticmethod
    def findByIdUpdate(userId: int, payload: dict):
        db: Session = SessionLocal()
        user = db.query(User).filter(User.id == userId,
                                     User.isDeleted==False
                                     ).first()
        if not user:
            return None  # or raise HTTPException

        for key, value in payload.items():
            setattr(user, key, value)

        db.commit()
        db.refresh(user)
        return jsonable_encoder(user)
    
    @staticmethod
    def findById(userId: int):
        db: Session = SessionLocal()
        try:
            user = db.query(User).filter(User.id == userId,
                                         User.isDeleted==False).first()
            return jsonable_encoder(user)
        except Exception as e:
            print(e)
            
    @staticmethod
    def findByNumber(phone_number: str) :
        db: Session = SessionLocal()
        try:
            user = db.query(User).filter(
                                        User.phone_number == phone_number,
                                        User.isDeleted == False
                                        ).first()
            return jsonable_encoder(user)
        except Exception as e:
            print(e)
            
            
    @staticmethod
    def getList(find=None, option = {"page": 1, "limit": 10}):
        db: Session = SessionLocal()
        try:
            user = (
            db.query(User)
            .filter(User.isDeleted == False,
                    User.userType!=userType.admin)
            .order_by(desc(User.created_at))   #  correct
            .all())
            data = jsonable_encoder(user)
            return PaginationRsponse.returnData(data,option)
        except Exception as e:
            print(e)


UserService = userService()
