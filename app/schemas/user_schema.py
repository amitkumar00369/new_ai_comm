from pydantic import BaseModel, Field
from typing import Optional,Literal

class SignupValidation(BaseModel):
    phone_number: str
    country_code: Optional[str] = Field(default="+971")
class VerifyOtps(BaseModel):
    type: Literal["email", "phone"]
    userId: int
    otp: int
    

class changePasswordValidation(BaseModel):
    new_password: str
    old_password: str
class changeEmail(BaseModel):
    old_email: str
    new_email: str


