import enum
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    hq_city = Column(String, nullable=True)
    hq_state = Column(String, nullable=True)
    hq_country = Column(String, nullable=True)

    contacts = relationship("Contact", back_populates="company")
    applications = relationship("Application", back_populates="company")

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    name = Column(String, nullable=False)
    role = Column(String, nullable=True)          # recruiter / hiring manager / interviewer
    email = Column(String, nullable=True)
    linkedin_url = Column(String, nullable=True)

    company = relationship("Company", back_populates="contacts")
    applications = relationship("Application", back_populates="contact")

class ApplicationStatus(str, enum.Enum):
    applied = "applied"
    interview= "interview"
    offer = "offer"
    rejected = "rejected"

class Application(Base):
    __tablename__= "applications"

    id = Column(Integer, primary_key = True, index = True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    contact_id = Column(Integer, ForeignKey("contacts.id"), nullable=True)

    role_title = Column(String, nullable=False)
    status = Column(Enum(ApplicationStatus), nullable=False, default=ApplicationStatus.applied)
    date_applied = Column(DateTime(timezone=True), server_default=func.now())
    date_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    source = Column(String, nullable=True)       # referral, LinkedIn, company site, etc.
    notes = Column(String, nullable=True)
    url = Column(String, nullable=True)

    company = relationship("Company", back_populates="applications")
    contact = relationship("Contact", back_populates="applications")
    status_history = relationship("StatusHistory", back_populates="application")

class StatusHistory(Base):
    __tablename__ = "status_history"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=False)
    from_status = Column(Enum(ApplicationStatus), nullable=True)   # nullable — first entry has no "from"
    to_status = Column(Enum(ApplicationStatus), nullable=False)
    changed_at = Column(DateTime(timezone=True), server_default=func.now())

    application = relationship("Application", back_populates="status_history")