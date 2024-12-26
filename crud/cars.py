from fastapi import HTTPException
from sqlalchemy.orm import Session
import models, schemas

def get_cars(db: Session):
    return db.query(models.Car).all()

def create_car(db: Session, car: schemas.CarCreate):
    db_car = models.Car(**car.dict())
    db.add(db_car)
    db.commit()
    db.refresh(db_car)
    return db_car

def delete_car(db: Session, car_id: int):
    try:
        db_car = db.query(models.Car).filter(models.Car.id == car_id).first()
        if db_car:
            db.delete(db_car)
            db.commit()
            return db_car
        raise HTTPException(status_code=404, detail="Car not found")
    except Exception as e:
        print(f"Error deleting car: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete car")


def update_car(db: Session, car_id: int, car: schemas.CarUpdate):
    db_car = db.query(models.Car).filter(models.Car.id == car_id).first()
    if db_car:
        for key, value in car.dict(exclude_unset=True).items():
            setattr(db_car, key, value)
        db.commit()
        db.refresh(db_car)
        return db_car
    return None

