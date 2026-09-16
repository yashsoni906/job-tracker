from pydantic import BaseModel
from typing import Optional
from app.models import ApplicationStatus
from datetime import datetime

class CompanyBase(BaseModel):
    name: str
    hq_city: Optional[str] = None
    hq_state: Optional[str] = None
    hq_country: Optional[str] = None

class CompanyCreate(CompanyBase):
    pass

class Company(CompanyBase):
    id: int

    class Config:
        from_attributes = True

class ContactBase(BaseModel):
    name: str
    role: Optional[str] = None
    email: Optional[str] = None
    linkedin_url: Optional[str] = None

class ContactCreate(ContactBase):
    company_id: int

class Contact(ContactBase):
    id: int
    company_id: int

    class Config:
        from_attributes = True

class ApplicationBase(BaseModel):
    role_title: str
    status: ApplicationStatus = ApplicationStatus.applied
    source: Optional[str] = None
    notes: Optional[str] = None
    url: Optional[str] = None

class ApplicationCreate(ApplicationBase):
    company_id: int
    contact_id: Optional[int] = None

class Application(ApplicationBase):
    id: int
    company_id: int
    contact_id: Optional[int] = None
    date_applied: datetime
    date_updated: datetime

    class Config:
        from_attributes = True

class StatusHistory(BaseModel):
    id: int
    application_id: int
    from_status: Optional[ApplicationStatus] = None
    to_status: ApplicationStatus
    changed_at: datetime

    class Config:
        from_attributes = True