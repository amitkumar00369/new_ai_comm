from pydantic import BaseModel, Field
from typing import Optional,Literal

class CreateAgent(BaseModel):
    phone_number: Optional[str] = Field(
        default=None,
        pattern=r"^\d{7,15}$"
    )
    name: str
    country_code: Optional[str] = Field(
        default="+971",
        pattern=r"^\+\d{1,4}$"
    )
    plan_id: int
    
class AgentUpdate(BaseModel):
    id: int

    type: Literal["1", "2", "3"]
    # 1 -> update data
    # 2 -> block/unblock
    # 3 -> delete plan

    name: Optional[str] = None
    image: Optional[str] = None
    plan_id: Optional[int] = None
    

    

