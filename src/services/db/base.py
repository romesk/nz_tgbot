from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base, Session

from src import config

Base = declarative_base()


async def async_main():
    engine = create_async_engine(config.POSTGRES_URI, future=True)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    return engine

