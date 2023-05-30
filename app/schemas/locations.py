import re

from pydantic import BaseModel, Field

from app.helpers.exceptions import Exceptions


class ZipCode(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError("Str is required")
        if not re.fullmatch("\d{5}", v):
            raise Exceptions.WrongZipcode
        return str(v)

class CreateLocation(BaseModel):
    city: str = Field(..., title="City")
    state: str = Field(..., title="State")
    zipcode: ZipCode = Field(..., title="Zip code")
    longitude: float = Field(..., title="Longitude")
    latitude: float = Field(..., title="Latitude")

class Location(CreateLocation):
    id: int = Field(..., title=" Location ID")

    class Config:
        orm_mode = True
