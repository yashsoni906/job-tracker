from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.post("/", response_model=schemas.Contact)
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    return crud.create_contact(db, contact)


@router.get("/company/{company_id}", response_model=List[schemas.Contact])
def list_contacts_for_company(company_id: int, db: Session = Depends(get_db)):
    return crud.get_contacts_by_company(db, company_id)