from fastapi import HTTPException


class Exceptions:
    WrongZipcode = HTTPException(status_code=400, detail="Zip code must be a 5-digit string")
    ZipcodeIsUsed = HTTPException(status_code=400, detail="This zipcode is already registered")

    SamePointShipping = HTTPException(status_code=400, detail="Pickup and delivery locations must be different")
    
    CargoNotFound = HTTPException(status_code=404, detail="Cargo was not found")
    LocationNotFound = HTTPException(status_code=404, detail="Location was not found")
    VehicleNotFound = HTTPException(status_code=404, detail="Vehicle was not found")
    