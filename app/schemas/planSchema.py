from pydantic import BaseModel
from app.utils.enum import planType,periodType
from typing import Optional,Literal


class create(BaseModel):
    name: str
    planType: Literal[planType.free,planType.paid]
    period: Literal[periodType.default,periodType.monthly,periodType.quaterly,periodType.yearly]
    price: int