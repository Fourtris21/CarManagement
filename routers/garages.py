from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[schemas.Garage])
def read_garages(db: Session = Depends(get_db)):
    return crud.get_garages(db)

@router.post("/", response_model=schemas.Garage)
def create_garage(garage: schemas.GarageCreate, db: Session = Depends(get_db)):
    return crud.create_garage(db, garage)

@router.delete("/{garage_id}", response_model=schemas.Garage)
def delete_garage(garage_id: int, db: Session = Depends(get_db)):
    db_garage = crud.delete_garage(db, garage_id)
    return schemas.Garage.from_orm(db_garage)

@router.put("/{garage_id}", response_model=schemas.Garage)
def update_garage(garage_id: int, garage: schemas.GarageUpdate, db: Session = Depends(get_db)):
    updated_garage = crud.update_garage(db, garage_id, garage)
    if not updated_garage:
        raise HTTPException(status_code=404, detail="Garage not found")
    return schemas.Garage.from_orm(updated_garage)
