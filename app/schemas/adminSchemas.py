from pydantic import BaseModel, EmailStr, Field

class createAdmin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=3, max_length=50)
    
