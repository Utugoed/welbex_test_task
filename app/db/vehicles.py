from typing import List

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.orm import Session

from app.db.models import Vehicle


class Vehicles:
    
    @staticmethod
    async def insert_many(vehicles: List[dict], session: AsyncSession):
        vehicles_objs = [Vehicle(**vehicle) for vehicle in vehicles]
        
        session.add_all(vehicles_objs)
        await session.commit()
        return vehicles_objs

    @staticmethod
    async def get_all(session: AsyncSession):
        stmt = select(Vehicle).options(selectinload(Vehicle.location))
        
        result = await session.execute(stmt)
        vehicles = result.scalars().all()
        return vehicles
    
    @staticmethod
    def sync_get_all(session: Session):
        stmt = select(Vehicle)
        result = session.execute(stmt)
        vehicles = result.scalars().all()
        return vehicles
    
    @staticmethod
    async def move_vehicle(
        vehicle_id: int, new_location_id: int, session: AsyncSession
    ):
        stmt = update(Vehicle).where(Vehicle.id == vehicle_id)
        stmt = stmt.values(location_id = new_location_id)
        stmt = stmt.execution_options(synchronize_session="fetch")
        
        r = await session.execute(stmt)
        await session.commit()
        return r
    
    @staticmethod
    def sync_move_vehicles(
        new_locations_ids: list[int], vehicles_ids: list[int], session: Session
    ):
        for i, vehicle_id in enumerate(vehicles_ids):
            stmt = update(Vehicle).where(Vehicle.id == vehicle_id)
            stmt = stmt.values(location_id = new_locations_ids[i])
            session.execute(stmt)
        
        session.commit()

