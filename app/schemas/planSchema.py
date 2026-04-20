from pydantic import BaseModel
from app.utils.enum import planType,periodType
from typing import Optional,Literal


class create(BaseModel):
    name: str
    planType: Literal["0","1"]
    period: Literal[periodType.default,periodType.monthly,periodType.quaterly,periodType.yearly]
    price: int
class PlanUpdate(BaseModel):
    id: int

    type: Literal["1", "2", "3"]
    # 1 -> update data
    # 2 -> block/unblock
    # 3 -> delete plan

    name: Optional[str] = None

    planType: Optional[Literal["0","1"]] = None

    period: Optional[Literal[periodType.default,periodType.monthly,periodType.quaterly,periodType.yearly]] = None

    price: Optional[int] = None