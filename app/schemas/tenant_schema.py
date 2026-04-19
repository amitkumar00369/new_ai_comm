from pydantic import BaseModel, Field
from typing import Optional,Literal
from app.utils.enum import bussinesType

class create(BaseModel):
    business_name: Literal[
        "0","1","2","3","4","5","6","7","8","9","10","11"
    ]