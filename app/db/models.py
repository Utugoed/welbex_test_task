from sqlalchemy import (
    DECIMAL, Column, ForeignKey, Integer, String, Text
)
from sqlalchemy.orm import relationship

from app.db import Base


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)

    
class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    city = Column(String)
    state = Column(String)
    zipcode = Column(String(5), unique=True)
    latitude = Column(DECIMAL(8, 6))
    longitude = Column(DECIMAL(9, 6))


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    uid = Column(String(5), unique=True)
    capacity = Column(Integer)
    location_id = Column(Integer, ForeignKey("locations.id"))

    location = relationship("Location", foreign_keys=[location_id])


class Cargo(Base):
    __tablename__ = "cargos"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    weight = Column(Integer)
    description = Column(Text)
    pickup_id = Column(Integer, ForeignKey("locations.id"))
    delivery_id = Column(Integer, ForeignKey("locations.id"))

    pickup = relationship("Location", foreign_keys=[pickup_id])
    delivery = relationship("Location", foreign_keys=[delivery_id])
