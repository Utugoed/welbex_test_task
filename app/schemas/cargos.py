from typing import List, Optional
from pydantic import BaseModel, Field

from app.schemas.locations import Location, ZipCode
from app.schemas.vehicles import CargoVehicle


class CreateCargo(BaseModel):
    pickup_zip: ZipCode = Field(..., title="Pick up location ID")
    delivery_zip: ZipCode = Field(..., title="Delivery loation ID")
    weight: int = Field(..., title="Weight", gt=0, lt=100001)
    description: str = Field(..., title="Description")

class UpdateCargo(BaseModel):
    weight: Optional[int] = Field(None, title="Weight", gt=0, lt=100001)
    description: Optional[str] = Field(None, title="Description")

class CargoRepresentation(BaseModel):
    pickup: Location = Field(..., title="Pickup location")
    delivery: Location = Field(..., title="Delivery location")
    weight: int = Field(..., title="Weight")

    class Config:
        orm_mode = True

class CargoListItem(CargoRepresentation):
    nearest_vehicles: int = Field(
        ..., title="Vehicles amount", description="Nearest vehicles amount"
    )

class CargoItem(CargoRepresentation):
    description: str = Field(..., title="Description")
    vehicles: List[CargoVehicle] = Field(..., title="List of vehicles")
