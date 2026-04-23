import pandas as pd
import os

from fastapi.concurrency import run_in_threadpool
from sqlalchemy import desc
from sqlalchemy.orm import Session
from stripe import PlanService

from app.models.tenant_model import Tenant
from app.models.user_model import User
from app.utils.constants import generateLeadId
from app.utils.pagination import PaginationRsponse
from ..models.lead_model import Lead
from core.database import SessionLocal
from fastapi.encoders import jsonable_encoder
from app.utils.enum import userType
def create_lead(user_number,agent_number,tenant_number=None, tenant_id=None,serviceId=None,source="1"):
    lead = {
        "leadId": generateLeadId(user_number),
        "user_id": tenant_id,
        "phone": user_number,
        "tenant_phone": tenant_number,
        "serviceId": serviceId,
        "agent_number": agent_number,
        "source": source
    }
    print("Creating lead with data:", lead)

    db: Session = SessionLocal()
    try:
        newLead = Lead(**lead)
        db.add(newLead)
        db.commit()
        db.refresh(newLead)
        return jsonable_encoder(newLead)
    except Exception as e:
        db.rollback()
    finally:
        db.close()
        
def get_leads_by_user_id(user_id):
    db: Session = SessionLocal()
    try:
        #  Get tenant_id for the user
        result = (
            db.query(Lead)
            .filter(Lead.user_id == user_id)
            .order_by(desc(Lead.created_at))        
            .all())
        return jsonable_encoder(result)
    except Exception as e:
        print("Error fetching leads:", e)
        return []
    finally:
        db.close()