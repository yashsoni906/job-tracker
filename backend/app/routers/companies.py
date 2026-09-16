from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/companies", tags=["companies"])


@router.post("/", response_model=schemas.Company)
def create_company(company: schemas.CompanyCreate, db: Session = Depends(get_db)):
    return crud.create_company(db, company)


@router.get("/", response_model=List[schemas.Company])
def list_companies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_companies(db, skip=skip, limit=limit)


@router.get("/{company_id}", response_model=schemas.Company)
def get_company(company_id: int, db: Session = Depends(get_db)):
    db_company = crud.get_company(db, company_id)
    if db_company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return db_company