from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from app import models, schemas


def create_company(db: Session, company: schemas.CompanyCreate):
    db_company = models.Company(**company.model_dump())
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company


def get_company(db: Session, company_id: int):
    return db.query(models.Company).filter(models.Company.id == company_id).first()


def get_companies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Company).offset(skip).limit(limit).all()

def create_contact(db: Session, contact: schemas.ContactCreate):
    db_contact = models.Contact(**contact.model_dump())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


def get_contacts_by_company(db: Session, company_id: int):
    return db.query(models.Contact).filter(models.Contact.company_id == company_id).all()

def create_application(db: Session, application: schemas.ApplicationCreate):
    db_application = models.Application(**application.model_dump())
    db.add(db_application)
    db.commit()
    db.refresh(db_application)

    # log the initial status into StatusHistory
    history = models.StatusHistory(
        application_id=db_application.id,
        from_status=None,
        to_status=db_application.status,
    )
    db.add(history)
    db.commit()

    return db_application


def get_application(db: Session, application_id: int):
    return db.query(models.Application).filter(models.Application.id == application_id).first()


def get_applications(
    db: Session,
    status: schemas.ApplicationStatus = None,
    company_id: int = None,
    sort_by: str = "date_applied",
    order: str = "desc",
    skip: int = 0,
    limit: int = 100,
):
    query = db.query(models.Application)

    if status:
        query = query.filter(models.Application.status == status)
    if company_id:
        query = query.filter(models.Application.company_id == company_id)

    sort_column = getattr(models.Application, sort_by, models.Application.date_applied)
    query = query.order_by(desc(sort_column) if order == "desc" else asc(sort_column))

    return query.offset(skip).limit(limit).all()


def update_application_status(db: Session, application_id: int, new_status: schemas.ApplicationStatus):
    db_application = get_application(db, application_id)
    if not db_application:
        return None

    old_status = db_application.status
    db_application.status = new_status
    db.commit()
    db.refresh(db_application)

    history = models.StatusHistory(
        application_id=application_id,
        from_status=old_status,
        to_status=new_status,
    )
    db.add(history)
    db.commit()

    return db_application