

from typing import Generic, TypeVar

from sqlalchemy import select
from models.base_model import BaseModel
from repository.connection_manager import ConnectionManager
from functools import wraps


def exception_handler_decorator(method):
    @wraps(method)
    async def wrapper(self, *args, **kwargs):
        try:
            return await method(self, *args, **kwargs)
        except Exception as e:
            if self.connection_manager.transaction_started:
                await self.connection_manager.end_transaction(commit=False)
            raise e
    return wrapper


T = TypeVar('T', bound=BaseModel)


class BaseRepository(Generic[T]):
    def __init__(self, clazz: T):
        self.connection_manager = ConnectionManager()
        self.clazz = clazz

    @exception_handler_decorator
    async def create(self, data: T) -> T:
        async with self.connection_manager.get_session() as session:
            session.add(data)
            await session.flush()
            await session.refresh(data)
            return data

    @exception_handler_decorator
    async def get_by_id(self, id: int) -> T:
        async with self.connection_manager.get_session() as session:
            result = await session.get(self.clazz, id)
            return result

    @exception_handler_decorator
    async def get_all(self) -> list[T]:
        async with self.connection_manager.get_session() as session:
            stmt = select(self.clazz)
            result = await session.execute(stmt)
            return result.scalars().all()

    @exception_handler_decorator
    async def update(self, id: int, data: T) -> T:
        async with self.connection_manager.get_session() as session:
            db_obj = await session.get(self.clazz, id)
            if not db_obj:
                raise ValueError(f"{T.__name__} with id {id} not found")

            for key in data.__dict__.keys():
                if key == 'id' or key.startswith('_'):
                    continue
                value = getattr(data, key)
                if value is not None:
                    setattr(db_obj, key, value)

            await session.flush()
            await session.refresh(db_obj)
            return db_obj

    @exception_handler_decorator
    async def delete(self, id: int) -> None:
        """Delete a record."""
        async with self.connection_manager.get_session() as session:
            db_obj = await session.get(self.clazz, id)
            if not db_obj:
                raise ValueError(f"{T.__name__} with id {id} not found")
            await session.delete(db_obj)
            await session.flush()

    async def start_transaction(self):
        await self.connection_manager.start_transaction()

    async def end_transaction(self, commit=True):
        await self.connection_manager.end_transaction(commit)

    async def rollback_transaction(self):
        await self.connection_manager.end_transaction(commit=False)
