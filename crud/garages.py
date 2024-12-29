from datetime import datetime
from typing import List

from fastapi import HTTPException
from sqlalchemy import extract
from sqlalchemy.orm import Session
import models, schemas

def get_garages(db: Session, city: str = None):
    query = db.query(models.Garage)

    if city:
        query = query.filter(models.Garage.city == city)

    return query.all()

def get_daily_availability_report(
    db: Session, garage_id: int, start_date: datetime, end_date: datetime
) -> List[schemas.DailyAvailabilityReport]:

    maintenance_data = (
        db.query(models.Maintenance)
        .filter(
            models.Maintenance.garageId == garage_id,
            extract("year", models.Maintenance.scheduledDate) >= start_date.year,
            extract("month", models.Maintenance.scheduledDate) >= start_date.month,
            extract("day", models.Maintenance.scheduledDate) >= start_date.day,
            extract("year", models.Maintenance.scheduledDate) <= end_date.year,
            extract("month", models.Maintenance.scheduledDate) <= end_date.month,
            extract("day", models.Maintenance.scheduledDate) <= end_date.day,
        )
        .all()
    )
    garage_data = db.query(models.Garage).filter(models.Garage.id == garage_id).first()
    # import pdb; pdb.set_trace()
    # Генериране на репорт на база дати
    report = {}
    year_month_day = None
    for maintenance in maintenance_data:
        year_month_day = datetime.strptime(maintenance.scheduledDate, "%Y-%m-%d")
        if year_month_day not in report:
            report[year_month_day] = {
                "requests": 0,
                "capacity": garage_data.capacity
            }
        report[year_month_day]["requests"] += 1
        report[year_month_day]["capacity"] -= 1

    return [
        schemas.DailyAvailabilityReport(date=str(date)[:10], requests=props["requests"], availableCapacity=props["capacity"])
        for date, props in sorted(report.items())
    ]

def create_garage(db: Session, garage: schemas.Garage):
    db_garage = models.Garage(**garage.dict())
    db.add(db_garage)
    db.commit()
    db.refresh(db_garage)
    return db_garage

def delete_garage(db: Session, garage_id: int):
    try:
        db_garage = db.query(models.Garage).filter(models.Garage.id == garage_id).first()
        if db_garage:
            db.delete(db_garage)
            db.commit()
            return db_garage
        raise HTTPException(status_code=404, detail="Garage not found")
    except Exception as e:
        print(f"Error deleting garage: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete garage")


def update_garage(db: Session, garage_id: int, garage: schemas.GarageUpdate):
    db_garage = db.query(models.Garage).filter(models.Garage.id == garage_id).first()
    if db_garage:
        for key, value in garage.dict(exclude_unset=True).items():
            setattr(db_garage, key, value)
        db.commit()
        db.refresh(db_garage)
        return db_garage
    return None

