from sqlalchemy import create_engine
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings


USER = settings.POSTGRES_USER
PASSWORD = settings.POSTGRES_PASSWORD
HOST = settings.POSTGRES_HOST
PORT = settings.POSTGRES_PORT
TABLE = settings.TABLE

DATABASE_URL = f"postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}:{PORT}/{TABLE}"


engine = create_async_engine(url=DATABASE_URL)
Base = declarative_base()
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def init_models():
    async with engine.begin() as conn:
        try:
            await conn.run_sync(Base.metadata.create_all)
        except ProgrammingError:
            ...

async def get_session():
    async with async_session() as session:
        yield session


SYNC_DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{TABLE}"

sync_engine = create_engine(url=SYNC_DATABASE_URL)
sync_session = sessionmaker(engine)

def get_sync_session():
    with sync_session() as session:
        yield session