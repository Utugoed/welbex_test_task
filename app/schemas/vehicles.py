from pydantic import BaseModel, Field

from app.schemas.locations import ZipCode


class UpdateVehicle(BaseModel):
    location_zip: ZipCode = Field(..., title="Location zip code")

class CargoVehicle(BaseModel):
    uid: str = Field(..., title="UID")
    distance: float = Field(..., title="Distance to cargo")