from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import schemas
from crud import cars
from database import SessionLocal
from models import Car, Garage

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[schemas.Car])
def read_cars_filter(carMake: str = None, garageId: int = None, fromYear: int = None, toYear: int = None, db: Session = Depends(get_db)):
    cars_all = cars.get_cars_filter(db, carMake, garageId, fromYear, toYear)
    return cars_all

@router.post("/", response_model=schemas.Car)
def create_car(car: schemas.CarCreate, db: Session = Depends(get_db)):
    db_car = Car(
        make=car.make,
        model=car.model,
        productionYear=car.productionYear,
        licensePlate=car.licensePlate,
        garageIds=car.garageIds
    )
    if car.garageIds:
        db_car.garages = db.query(Garage).filter(Garage.id.in_(car.garageIds)).all()
    db.add(db_car)
    db.commit()
    db.refresh(db_car)
    return db_car

@router.delete("/{car_id}", response_model=schemas.Car)
def delete_car(car_id: int, db: Session = Depends(get_db)):
    db_car = cars.delete_car(db, car_id)
    return schemas.Car.from_orm(db_car)

@router.put("/{car_id}", response_model=schemas.Car)
def update_car(car_id: int, car: schemas.CarUpdate, db: Session = Depends(get_db)):
    updated_car = cars.update_car(db, car_id, car)
    if not updated_car:
        raise HTTPException(status_code=404, detail="Car not found")
    return schemas.Car.from_orm(updated_car)
