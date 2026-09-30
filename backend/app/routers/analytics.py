from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud
from app.database import get_db

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/response-rate")
def response_rate(db: Session = Depends(get_db)):
    return crud.get_response_rate(db)


@router.get("/weekly-velocity")
def weekly_velocity(db: Session = Depends(get_db)):
    return crud.get_weekly_velocity(db)


@router.get("/avg-time-to-response")
def avg_time_to_response(db: Session = Depends(get_db)):
    return crud.get_avg_time_to_response(db)