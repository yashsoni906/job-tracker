from sqlalchemy.orm import Session
from sqlalchemy import asc, desc, func
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

def get_response_rate(db: Session):
    total = db.query(models.Application).count()
    if total == 0:
        return {"total_applications": 0, "responded": 0, "response_rate": 0.0}

    responded = db.query(models.Application).filter(
        models.Application.status != models.ApplicationStatus.applied
    ).count()

    return {
        "total_applications": total,
        "responded": responded,
        "response_rate": round((responded / total) * 100, 1),
    }

def get_weekly_velocity(db: Session):
    results = (
        db.query(
            func.date_trunc('week', models.Application.date_applied).label('week'),
            func.count(models.Application.id).label('count')
        )
        .group_by('week')
        .order_by('week')
        .all()
    )
    return [{"week": row.week, "count": row.count} for row in results]

def get_avg_time_to_response(db: Session):
    # subquery: first two status_history rows per application, ordered by time
    from sqlalchemy import select

    applications_with_response = (
        db.query(models.Application.id)
        .join(models.StatusHistory)
        .filter(models.StatusHistory.from_status.isnot(None))  # has had at least one transition
        .distinct()
        .all()
    )

    if not applications_with_response:
        return {"average_days_to_response": None, "sample_size": 0}

    diffs = []
    for (app_id,) in applications_with_response:
        history = (
            db.query(models.StatusHistory)
            .filter(models.StatusHistory.application_id == app_id)
            .order_by(models.StatusHistory.changed_at)
            .limit(2)
            .all()
        )
        if len(history) == 2:
            delta = history[1].changed_at - history[0].changed_at
            diffs.append(delta.total_seconds() / 86400)  # convert to days

    avg_days = round(sum(diffs) / len(diffs), 1) if diffs else None

    return {"average_days_to_response": avg_days, "sample_size": len(diffs)}