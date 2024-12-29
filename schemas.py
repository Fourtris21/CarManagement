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
    garageIds: list[int]

class CarUpdate(BaseModel):
    make: str | None = None
    model: str | None = None
    year: str | None = None
    garageIds: list[int] | None = None

class Car(CarBase):
    id: int
    garages: List[Garage] = []

    class Config:
        from_attributes = True

class MaintenanceBase(BaseModel):
    scheduledDate: str
    serviceType: str
    carId: int
    garageId: int

class MaintenanceCreate(MaintenanceBase):
    pass

class MaintenanceUpdate(BaseModel):
    scheduledDate: str | None = None
    serviceType: str | None = None
    carId: int | None = None
    garageId: int | None = None

class MonthlyRequestsReport(BaseModel):
    yearMonth: str
    requests: int
class Maintenance(MaintenanceBase):
    id: int

    class Config:
        from_attributes = True
