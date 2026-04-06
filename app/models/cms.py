

from turtle import title

from sqlalchemy import Column, Integer, String, Text,Enum

from app.models.base_models import BaseMixin
from core.database import Base
from app.utils.enum import cmsType

class cms (Base, BaseMixin):
    __tablename__ = "cms"

    id = Column(Integer, primary_key=True, index=True)
    pageName = Column(Enum(cmsType), unique=True)  # aboutUs / privacyPolicy / termsAndConditions / contactUs
    title = Column(String)
    content = Column(Text)
    email = Column(String)
    phone = Column(String)
    countryCode = Column(String)
