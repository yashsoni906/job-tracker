from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/applications", tags=["applications"])


@router.post("/", response_model=schemas.Application)
def create_application(application: schemas.ApplicationCreate, db: Session = Depends(get_db)):
    return crud.create_application(db, application)


@router.get("/", response_model=List[schemas.Application])
def list_applications(
    status: Optional[schemas.ApplicationStatus] = None,
    company_id: Optional[int] = None,
    sort_by: str = "date_applied",
    order: str = "desc",
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return crud.get_applications(
        db,
        status=status,
        company_id=company_id,
        sort_by=sort_by,
        order=order,
        skip=skip,
        limit=limit,
    )


@router.get("/{application_id}", response_model=schemas.Application)
def get_application(application_id: int, db: Session = Depends(get_db)):
    db_application = crud.get_application(db, application_id)
    if db_application is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return db_application


@router.patch("/{application_id}/status", response_model=schemas.Application)
def update_status(application_id: int, new_status: schemas.ApplicationStatus, db: Session = Depends(get_db)):
    db_application = crud.update_application_status(db, application_id, new_status)
    if db_application is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return db_application