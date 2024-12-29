from typing import List, Dict

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import schemas
from crud import maintenance
from crud.maintenance import get_monthly_requests_report
from database import SessionLocal
from datetime import datetime

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[schemas.Maintenance])
def read_maintenance(carId: int = None, garageId: int = None, fromDate: str = None, toDate: str = None, db: Session = Depends(get_db)):
    return maintenance.get_maintenance(db, carId, garageId, fromDate, toDate)

@router.get("/monthlyRequestsReport", response_model=List[schemas.MonthlyRequestsReport])
def monthly_requests_report(
    garageId: int,
    startMonth: str = Query(..., description="Start month in YYYY-MM format"),
    endMonth: str = Query(..., description="End month in YYYY-MM format"),
    db: Session = Depends(get_db)
):
    try:
        start_date = datetime.strptime(startMonth, "%Y-%m")
        end_date = datetime.strptime(endMonth, "%Y-%m")
    except ValueError:
        raise HTTPException(
            status_code=400, detail="Invalid date format. Use YYYY-MM format."
        )

    if start_date > end_date:
        raise HTTPException(
            status_code=400, detail="Start month cannot be after end month."
        )

    report = get_monthly_requests_report(db, garageId, start_date, end_date)

    return report

@router.post("/", response_model=schemas.Maintenance)
def create_maintenance(maintenance1: schemas.MaintenanceCreate, db: Session = Depends(get_db)):
    return maintenance.create_maintenance(db, maintenance1)

@router.delete("/{maintenance_id}", response_model=schemas.Maintenance)
def delete_maintenance(maintenance_id: int, db: Session = Depends(get_db)):
    db_maintenance = maintenance.delete_maintenance(db, maintenance_id)
    return schemas.Maintenance.from_orm(db_maintenance)

@router.put("/{maintenance_id}", response_model=schemas.Maintenance)
def update_maintenance(maintenance_id: int, maintenance1: schemas.MaintenanceUpdate, db: Session = Depends(get_db)):
    updated_maintenance = maintenance.update_maintenance(db, maintenance_id, maintenance1)
    if not updated_maintenance:
        raise HTTPException(status_code=404, detail="Maintenance not found")
    return schemas.Maintenance.from_orm(updated_maintenance)
