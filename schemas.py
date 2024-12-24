from pydantic import BaseModel
from typing import Optional

class GarageBase(BaseModel):
    name: str
    city: str
    capacity: int

class GarageCreate(GarageBase):
    pass

class Garage(GarageBase):
    id: int

    class Config:
        from_attributes = True

class GarageUpdate(BaseModel):
    name: str | None = None
    city: str | None = None
    capacity: int | None = None

class CarBase(BaseModel):
    make: str
    model: str
    year: int
    garage_id: Optional[int]

class CarCreate(CarBase):
    pass

class Car(CarBase):
    id: int

    class Config:
        orm_mode = True

class MaintenanceBase(BaseModel):
    date: str
    car_id: int
    garage_id: int

class MaintenanceCreate(MaintenanceBase):
    pass

class Maintenance(MaintenanceBase):
    id: int

    class Config:
        orm_mode = True
