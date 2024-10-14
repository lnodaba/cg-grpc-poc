
import asyncio
from contextlib import asynccontextmanager
import oracledb

from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from models.base_model import Base
from custom_logger import logger

from config import (
    DATABASE_HOST, NATIVE_SQL_DEBUG, DATABASE_PORT, DATABASE, USER, PASSWORD, MIN_POOL_SIZE,
    MAX_POOL_SIZE,
    POOL_INCREMENT
)


pool = oracledb.create_pool(
    user=USER, password=PASSWORD,
    host=DATABASE_HOST, port=DATABASE_PORT, service_name=DATABASE,
    min=MIN_POOL_SIZE, max=MAX_POOL_SIZE, increment=POOL_INCREMENT
)

engine = create_async_engine(
    "oracle+oracledb://",
    creator=pool.acquire,
    poolclass=NullPool,
    echo=NATIVE_SQL_DEBUG
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def init_db():

    tries = 0
    while True:

        try:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
                logger.info("Database tables initialized successfully.")
                return
        except Exception as e:
            logger.error("Could not sync database")
            logger.info("Retrying in 5 seconds...")
            if tries == 3:
                logger.error(f"Error initializing database: {e}")
                raise
            tries += 1
            await asyncio.sleep(5)


@asynccontextmanager
async def get_session() -> AsyncSession:
    session = AsyncSessionLocal()
    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()


async def close_pool():
    pool.close()
    logger.info("Database pool closed")
