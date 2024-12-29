from sqlalchemy import Column, Integer, String, Date, ForeignKey, PickleType, Table
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import relationship
from database import Base

# Таблица за връзка между Car и Garage
car_garage = Table(
    "car_garage",
    Base.metadata,
    Column("car_id", Integer, ForeignKey("cars.id"), primary_key=True),
    Column("garage_id", Integer, ForeignKey("garages.id"), primary_key=True)
)


class Garage(Base):
    __tablename__ = "garages"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    city = Column(String, index=True)
    location = Column(String, index=True)
    capacity = Column(Integer)
    cars = relationship(
        "Car",
        secondary="car_garage",
        back_populates="garages"
    )

class Car(Base):
    __tablename__ = "cars"
    id = Column(Integer, primary_key=True, index=True)
    make = Column(String, index=True)
    model = Column(String, index=True)
    productionYear = Column(Integer, index=True)
    licensePlate = Column(String, index=True)
    garageIds = Column(MutableList.as_mutable(PickleType), ForeignKey("garages.id"), default=[])
    garages = relationship(
        "Garage",
        secondary="car_garage",
        back_populates="cars"
    )

class Maintenance(Base):
    __tablename__ = "maintenances"
    id = Column(Integer, primary_key=True, index=True)
    scheduledDate = Column(String, index=True)
    serviceType = Column(String, index=True)
    carId = Column(Integer, ForeignKey("cars.id"))
    garageId = Column(Integer, ForeignKey("garages.id"))
