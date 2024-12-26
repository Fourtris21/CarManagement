from pydantic import BaseModel
from typing import Optional, List


class GarageBase(BaseModel):
    name: str
    city: str
    location: str
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
    location: str | None = None
    capacity: int | None = None

class CarBase(BaseModel):
    make: str
    model: str
    productionYear: int
    licensePlate: str


class CarCreate(CarBase):
    garageIds: List[int] = []

class CarUpdate(BaseModel):
    make: str | None = None
    model: str | None = None
    year: str | None = None
    garage_id: Optional[int] | None = None

class Car(CarBase):
    id: int
    garages: List[Garage] = []

    class Config:
        from_attributes = True

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
