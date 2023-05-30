from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.db.locations import Locations
from app.db.vehicles import Vehicles
from app.helpers.exceptions import Exceptions

from app.schemas.responses import ResponseModel
from app.schemas.vehicles import UpdateVehicle


vehicles_router = APIRouter()


@vehicles_router.patch("/{vehicle_id}", response_model=ResponseModel)
async def update_vehicle(
    input_data: UpdateVehicle,
    vehicle_id: int,
    session: AsyncSession = Depends(get_session)
):
    new_location = await Locations.get_one(zip_code=input_data.location_zip, session=session)
    if not new_location:
        raise Exceptions.LocationNotFound
    
    result = await Vehicles.move_vehicle(
        vehicle_id=vehicle_id, new_location_id=new_location.id, session=session
    )
    if not result.rowcount:
        raise Exceptions.VehicleNotFound
    return {
        "OK": True,
        "id": vehicle_id
    }
