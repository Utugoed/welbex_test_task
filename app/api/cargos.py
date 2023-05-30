from typing import List, Optional

from fastapi import APIRouter, Depends
from geopy.distance import distance
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import settings

from app.db import get_session
from app.db.cargos import Cargos
from app.db.locations import Locations
from app.db.vehicles import Vehicles

from app.helpers.exceptions import Exceptions
from app.schemas.cargos import (
    CargoItem, CargoListItem, CreateCargo, UpdateCargo
)
from app.schemas.responses import ResponseModel


cargos_router = APIRouter()


@cargos_router.post("/", response_model=ResponseModel)
async def new_cargo(
    input_data: CreateCargo,
    session: AsyncSession = Depends(get_session)
):
    if input_data.pickup_zip == input_data.delivery_zip:
        raise Exceptions.SamePointShipping
    
    pickup = await Locations.get_one(zip_code=input_data.pickup_zip, session=session)
    delivery = await Locations.get_one(zip_code=input_data.delivery_zip, session=session)

    if not (pickup and delivery):
        raise Exceptions.LocationNotFound
    
    cargo_dict = {
        "pickup_id": pickup.id,
        "delivery_id": delivery.id,
        "weight": input_data.weight,
        "description": input_data.description
    }
    cargo = await Cargos.insert_one(cargo=cargo_dict, session=session)
    return {
        "OK": True,
        "id": cargo.id
    }


@cargos_router.get("/", response_model=List[CargoListItem])
async def cargos_list(
    weight_gt: int = 0,
    weight_lt: int = 0,
    miles_gt: int = 0,
    miles_lt: int = 0,
    session: AsyncSession = Depends(get_session)
):
    weight_filters = {
        "lt": weight_lt,
        "gt": weight_gt
    }
    cargos = await Cargos.get_all(weight_filters=weight_filters, session=session)
    vehicles = await Vehicles.get_all(session=session)

    cargos_list = list(cargos)
    vehicles_coors = [
        (vehicle.location.latitude, vehicle.location.longitude) 
        for vehicle in vehicles
    ]
    
    for cargo in cargos_list:
        cargo.nearest_vehicles = 0
        cargo_coors = (cargo.pickup.latitude, cargo.pickup.longitude)
        
        for vehicle_coors in vehicles_coors:
            vehicle_distance = distance(vehicle_coors, cargo_coors).miles
            if miles_gt or miles_lt:
                not_gt = (vehicle_distance <= miles_gt) * miles_gt
                not_lt = (vehicle_distance >= miles_lt) * miles_lt
                if not_gt or not_lt:
                    continue
                cargo.nearest_vehicles += 1
            elif vehicle_distance <= settings.SEARCH_CIRCLE_RADIUS:
                cargo.nearest_vehicles += 1

    return cargos_list


@cargos_router.get("/{cargo_id}", response_model=CargoItem)
async def cargo(
    cargo_id: int,
    session: AsyncSession = Depends(get_session)
):
    cargo = await Cargos.get_one(cargo_id=cargo_id, session=session)
    vehicles = await Vehicles.get_all(session=session)

    vehicles_items = [{
        "uid": vehicle.uid,
        "distance": distance(
            (cargo.pickup.latitude, cargo.pickup.longitude),
            (vehicle.location.latitude, vehicle.location.longitude)
        ).miles
    } for vehicle in vehicles]

    cargo.vehicles = vehicles_items
    return cargo


@cargos_router.patch("/{cargo_id}", response_model=ResponseModel)
async def update_cargo(
    input_data: UpdateCargo,
    cargo_id: int,
    session: AsyncSession = Depends(get_session)
):
    data_dict = input_data.dict(exclude_none=True)
    result = await Cargos.update_one(
        cargo_id=cargo_id, new_data=data_dict, session=session
    )

    if not result.rowcount:
        raise Exceptions.CargoNotFound
    
    return {
        "OK": True,
        "id": cargo_id
    }


@cargos_router.delete("/{cargo_id}", response_model=ResponseModel)
async def delete_cargo(
    cargo_id: int,
    session: AsyncSession = Depends(get_session)
):
    result = await Cargos.delete_one(cargo_id=cargo_id, session=session)

    if not result.rowcount:
        raise Exceptions.CargoNotFound
    
    return {
        "OK": True,
        "id": cargo_id
    }
