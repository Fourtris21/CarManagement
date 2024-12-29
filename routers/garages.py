from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import schemas
from crud import garages
from crud.garages import get_daily_availability_report
from database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[schemas.Garage])
def read_garages(city: str = None, db: Session = Depends(get_db)):
    return garages.get_garages(db, city)

@router.post("/", response_model=schemas.Garage)
def create_garage(garage: schemas.GarageCreate, db: Session = Depends(get_db)):
    return garages.create_garage(db, garage)

@router.delete("/{garage_id}", response_model=schemas.Garage)
def delete_garage(garage_id: int, db: Session = Depends(get_db)):
    db_garage = garages.delete_garage(db, garage_id)
    return schemas.Garage.from_orm(db_garage)

@router.put("/{garage_id}", response_model=schemas.Garage)
def update_garage(garage_id: int, garage: schemas.GarageUpdate, db: Session = Depends(get_db)):
    updated_garage = garages.update_garage(db, garage_id, garage)
    if not updated_garage:
        raise HTTPException(status_code=404, detail="Garage not found")
    return schemas.Garage.from_orm(updated_garage)

@router.get("/dailyAvailabilityReport", response_model=List[schemas.DailyAvailabilityReport])
def daily_requests_report(
    garageId: int,
    startDate: str = Query(..., description="Start date in YYYY-MM-dd format"),
    endDate: str = Query(..., description="End date in YYYY-MM-dd format"),
    db: Session = Depends(get_db)
):
    try:
        start_date = datetime.strptime(startDate, "%Y-%m-%d")
        end_date = datetime.strptime(endDate, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(
            status_code=400, detail="Invalid date format. Use YYYY-MM format."
        )

    if start_date > end_date:
        raise HTTPException(
            status_code=400, detail="Start month cannot be after end month."
        )

    report = get_daily_availability_report(db, garageId, start_date, end_date)

    return report
