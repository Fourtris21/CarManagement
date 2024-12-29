from fastapi import HTTPException
from sqlalchemy.orm import Session
import models, schemas

def get_garages(db: Session, city: str = None):
    query = db.query(models.Garage)

    if city:
        query = query.filter(models.Garage.city == city)

    return query.all()

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

