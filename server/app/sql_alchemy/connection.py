
from contextlib import asynccontextmanager
import oracledb

from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from models.base_model import Base
from cutom_logger import logger

from config import (
    HOST, NATIVE_SQL_DEBUG, PORT, DATABASE, USER, PASSWORD, MIN_POOL_SIZE,
    MAX_POOL_SIZE,
    POOL_INCREMENT
)


pool = oracledb.create_pool(
    user=USER, password=PASSWORD,
    host=HOST, port=PORT, service_name=DATABASE,
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
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables initialized successfully.")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise


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
    pass
