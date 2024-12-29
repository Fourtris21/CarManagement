from datetime import datetime
from typing import List

from fastapi import HTTPException
from sqlalchemy.sql import extract
from sqlalchemy.orm import Session
import models, schemas


def get_maintenance(db: Session, carId: int = None, garageId: int = None, fromDate: str = None, toDate: str = None):
    query = db.query(models.Maintenance)

    if carId:
        query = query.filter(models.Maintenance.carId == carId)
    if garageId:
        query = query.filter(models.Maintenance.garageId == garageId)
    if fromDate:
        from_date_obj = datetime.strptime(fromDate, "%Y-%m-%d")
        query = query.filter(models.Maintenance.scheduledDate >= from_date_obj)
    if toDate:
        to_date_obj = datetime.strptime(toDate, "%Y-%m-%d")
        query = query.filter(models.Maintenance.scheduledDate <= to_date_obj)

    return query.all()

def get_monthly_requests_report(
    db: Session, garage_id: int, start_date: datetime, end_date: datetime
) -> List[schemas.MonthlyRequestsReport]:

    maintenance_data = (
        db.query(models.Maintenance)
        .filter(
            models.Maintenance.garageId == garage_id,
            extract("year", models.Maintenance.scheduledDate) >= start_date.year,
            extract("month", models.Maintenance.scheduledDate) >= start_date.month,
            extract("year", models.Maintenance.scheduledDate) <= end_date.year,
            extract("month", models.Maintenance.scheduledDate) <= end_date.month,
        )
        .all()
    )

    report = {}
    year_month = None
    for maintenance in maintenance_data:
        year_month = datetime.strptime(maintenance.scheduledDate[:7], "%Y-%m")
        if year_month not in report:
            report[year_month] = 0
        report[year_month] += 1

    return [
        schemas.MonthlyRequestsReport(yearMonth=str(year_month)[:7], requests=count)
        for year_month, count in sorted(report.items())
    ]
def create_maintenance(db: Session, maintenance: schemas.Maintenance):
    db_maintenance = models.Maintenance(**maintenance.dict())
    db.add(db_maintenance)
    db.commit()
    db.refresh(db_maintenance)
    return db_maintenance

def delete_maintenance(db: Session, maintenance_id: int):
    try:
        db_maintenance = db.query(models.Maintenance).filter(models.Maintenance.id == maintenance_id).first()
        if db_maintenance:
            db.delete(db_maintenance)
            db.commit()
            return db_maintenance
        raise HTTPException(status_code=404, detail="Maintenance not found")
    except Exception as e:
        print(f"Error deleting maintenance: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete maintenance")


def update_maintenance(db: Session, maintenance_id: int, maintenance: schemas.MaintenanceUpdate):
    db_maintenance = db.query(models.Maintenance).filter(models.Maintenance.id == maintenance_id).first()
    if db_maintenance:
        for key, value in maintenance.dict(exclude_unset=True).items():
            setattr(db_maintenance, key, value)
        db.commit()
        db.refresh(db_maintenance)
        return db_maintenance
    return None

