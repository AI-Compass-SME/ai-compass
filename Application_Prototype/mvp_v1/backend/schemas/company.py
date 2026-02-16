from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional

class CompanyBase(BaseModel):
    company_name: str
    industry: str
    website: Optional[str] = None
    number_of_employees: str
    city: Optional[str] = None
    email: EmailStr

class CompanyCreate(CompanyBase):
    pass

class CompanyResponse(CompanyBase):
    company_id: int

    class Config:
        from_attributes = True
