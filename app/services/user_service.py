from sqlalchemy.orm import Session
from ..models.user_model import User
from core.database import SessionLocal
from fastapi.encoders import jsonable_encoder

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
    def getMlModel():
        db: Session = SessionLocal()
        try:
            results = db.query(User).order_by(User.id.asc()).all()
            return jsonable_encoder(results)
        finally:
            db.close()
    @staticmethod
    def getUserByEmail(email: str):
        db: Session = SessionLocal()
        return jsonable_encoder(db.query(User).filter(User.email == email and User.isEmailVerified==True).first())

    @staticmethod
    def findByIdUpdate(userId: int, payload: dict):
        db: Session = SessionLocal()
        user = db.query(User).filter(User.id == userId).first()
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
            user = db.query(User).filter(User.id == userId).first()
            return jsonable_encoder(user)
        except Exception as e:
            print(e)
    @staticmethod
    def findByNumber(phone_number: str) :
        db: Session = SessionLocal()
        try:
            user = db.query(User).filter(User.phone_number == phone_number).first()
            return jsonable_encoder(user)
        except Exception as e:
            print(e)
        



UserService = userService()
