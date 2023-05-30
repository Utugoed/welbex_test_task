import csv
import logging
import random
import string

from sqlalchemy.exc import IntegrityError

from app.config import settings
from app.db import async_session
from app.db.locations import Locations
from app.db.vehicles import Vehicles
from app.schemas.locations import CreateLocation


logger = logging.getLogger("events")


def gen_vehicle_uid(ex_uids:list):
    uid = f"{random.randint(1000, 9999)}{random.choice(string.ascii_uppercase)}"
    
    if uid not in ex_uids:
        ex_uids.append(uid)
        return uid
    
    if len(ex_uids) == 9000:
        return
    
    return gen_vehicle_uid(ex_uids)


def gen_vehicle(ex_uids: list):
    location_id = random.randint(1, settings.LOCATIONS_AMOUNT)
    uid = gen_vehicle_uid(ex_uids)
    capacity = random.randint(1, 1000)
    return {
        "location_id": location_id,
        "uid": uid,
        "capacity": capacity
    }


async def load_default_vehicles():
    
    logger.info("Getting existing vehicles")
    async with async_session() as session:
        ex_vehicles = list(await Vehicles.get_all(session=session))
    
    logger.info("Counting existing vehicles")

    registered_uids = [vehicle.uid for vehicle in ex_vehicles]
    required_amount = settings.BASE_VEHICLES_AMOUNT - len(ex_vehicles)

    logger.info("Generating new vehicles")
    new_vehicles = [gen_vehicle(registered_uids) for i in range(required_amount)]

    logger.info("Inserting new vehicles")
    async with async_session() as session:
        result = await Vehicles.insert_many(new_vehicles, session=session)

    return result


async def load_locations():

    logger.info("Opening default locations file")
    with open("uszips.csv", "r") as locations_file:
        reader = csv.reader(locations_file)
        
        logger.info("Inserting default locations from file")
        next(reader)
        async with async_session() as session:
            for row in reader:
                location = CreateLocation(
                    city=row[3],
                    state=row[5],
                    zipcode=row[0],
                    latitude=float(row[1]),
                    longitude=float(row[2])
                ).dict()
                r = await Locations.insert_one(location=location, session=session)
            try:
                await session.commit()        
            except IntegrityError:
                await session.rollback()
