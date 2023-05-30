from sqlalchemy import delete, select, update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models import Cargo

from app.helpers.exceptions import Exceptions


class Cargos:

    @staticmethod
    async def insert_one(cargo: dict, session: AsyncSession):
        new_cargo = Cargo(**cargo)
        
        session.add(new_cargo)
        await session.commit()
        return new_cargo

    @staticmethod
    async def get_all(weight_filters: dict, session: AsyncSession):
        stmt = select(Cargo)
        
        if weight_filters.get("gt"):
            stmt = stmt.where(Cargo.weight > weight_filters["gt"])
        if weight_filters.get("lt"):
            stmt = stmt.where(Cargo.weight < weight_filters["lt"])
        
        stmt = stmt.options(selectinload(Cargo.pickup))
        stmt = stmt.options(selectinload(Cargo.delivery))
        
        result = await session.execute(stmt)
        cargos = result.scalars().all()
        return cargos
    
    @staticmethod
    async def get_one(cargo_id: int, session: AsyncSession):
        stmt = select(Cargo).where(Cargo.id == cargo_id)
        stmt = stmt.options(selectinload(Cargo.pickup))
        stmt = stmt.options(selectinload(Cargo.delivery))
        
        result = await session.execute(stmt)
        try:
            cargo = result.scalars().one()
            return cargo
        except NoResultFound:
            raise Exceptions.CargoNotFound
    
    @staticmethod
    async def update_one(cargo_id: int, new_data: dict, session: AsyncSession):
        stmt = update(Cargo).where(Cargo.id == cargo_id)
        stmt = stmt.values(**new_data)

        result = await session.execute(stmt)
        await session.commit()
        return result

    @staticmethod
    async def delete_one(cargo_id: int, session: AsyncSession):
        stmt = delete(Cargo).where(Cargo.id == cargo_id)
        
        result = await session.execute(stmt)
        await session.commit()
        return result