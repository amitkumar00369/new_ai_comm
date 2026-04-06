import os

from sqlalchemy.orm import Session

from core.database import SessionLocal
import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv()
from ..models.sessionModel import sessionModel
from fastapi.encoders import jsonable_encoder




class sessionService:
    @staticmethod
    def createSession(payload:dict):
        payload['exp'] = datetime.utcnow() + timedelta(hours=24)
        payload['iat'] = datetime.utcnow()
        # print("paylload",payload)
        jwt_token = jwt.encode(payload, 'SECRET_KEY', algorithm="HS256")
        # print("tokens",jwt_token)

        return jwt_token

    @staticmethod
    def createRefreshSession(payload:dict):
        payload['exp'] = datetime.utcnow() + timedelta(days=30)
        payload['iat'] = datetime.utcnow()
        jwt_token = jwt.encode(payload, 'SECRET_KEY', algorithm="HS256")
        # print("tokens",jwt_token)
        return jwt_token

    @staticmethod
    def decodeSession(token: str) -> str:
        payload = jwt.decode(token, 'SECRET_KEY', algorithms=['HS256'])
        return payload['userId']

    @staticmethod
    def createSessionData(payload: dict):
        db: Session = SessionLocal()
        try:
            print("payload",payload)
            new_record = sessionModel(**payload)
            db.add(new_record)
            db.commit()
            db.refresh(new_record)
            return jsonable_encoder(new_record)
        except Exception as e:
            print(e)
    @staticmethod
    def deleteSession(token: str):
        db: Session = SessionLocal()
        try:
            session = db.query(sessionModel).filter(sessionModel.accessToken == token).first()

            if session:
                db.delete(session)
                db.commit()
                return True

            return False
        except Exception as e:
            print(e)

    @staticmethod
    def deleteSessionByUserId(userId: int):
        db: Session = SessionLocal()
        try:
            db.query(sessionModel).filter(sessionModel.userId == userId).delete(synchronize_session=False)
            db.commit()
            return True
        except Exception as e:
            print(e)

    @staticmethod
    def getAllSessionData():
        db: Session = SessionLocal()
        return jsonable_encoder(db.query(sessionModel).order_by(sessionModel.id.desc()).all())

    @staticmethod
    def getSessionData(token: str):
        # print("tttttttt",token)
        db: Session = SessionLocal()
        try:
            results = db.query(sessionModel).filter(sessionModel.accessToken==token).first()
            return jsonable_encoder(results)
        except Exception as e:
            print(e)




SessionService = sessionService()








