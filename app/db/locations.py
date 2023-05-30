from typing import List

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Location


class Locations:

    @staticmethod
    async def insert_one(location: dict, session: AsyncSession):
        location_obj = Location(**location)
        session.add(location_obj)
    
    @staticmethod
    async def get_one(zip_code: str, session: AsyncSession):
        query = select(Location).where(Location.zipcode == zip_code)
        result = await session.execute(query)
        try:
            location = result.scalars().one()
            return location
        except NoResultFound:
            return