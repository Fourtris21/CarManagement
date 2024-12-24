from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Garage(Base):
    __tablename__ = "garages"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    city = Column(String, index=True)
    capacity = Column(Integer)

class Car(Base):
    __tablename__ = "cars"
    id = Column(Integer, primary_key=True, index=True)
    make = Column(String, index=True)
    model = Column(String, index=True)
    year = Column(Integer)
    garage_id = Column(Integer, ForeignKey("garages.id"))
    garage = relationship("Garage")

class Maintenance(Base):
    __tablename__ = "maintenances"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, index=True)
    car_id = Column(Integer, ForeignKey("cars.id"))
    garage_id = Column(Integer, ForeignKey("garages.id"))
