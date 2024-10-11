

import grpc
from sqlalchemy import select
from custom_logger import logger

from sql_alchemy.connection import get_session
from services.proto import acronyms_pb2
from datetime import date, datetime
from tortoise.exceptions import DoesNotExist
from decimal import Decimal


class BaseService:
    def __init__(self, OrmModel, GrpcModel, GrpcModelList):
        self.orm_model = OrmModel
        self.grpc_model = GrpcModel
        self.grpc_model_list = GrpcModelList

    async def create(self, request, context):
        async def create_query():
            create_dto = self.grpc_to_orm(request)
            async with get_session() as session:
                session.add(create_dto)
                await session.flush()
                await session.refresh(create_dto)
                logger.info(f"Object {create_dto} saved")
                return self.orm_to_grpc(create_dto)

        return await self._try_execute(create_query, request, context)

    async def get_all(self, request, context):
        async def get_all_query():
            async with get_session() as session:
                statement = select(self.orm_model)
                result = await session.execute(statement)
                orm_obj_list = result.scalars().all()
                dto_list = [
                    self.orm_to_grpc(orm_obj) for orm_obj in orm_obj_list
                ]
                return self.grpc_model_list(list=dto_list)

        return await self._try_execute(get_all_query, request, context)

    async def get_by_id(self, request, context):
        async def get_by_id_query():
            statement = select(self.orm_model).filter_by(id=request.id)
            async with get_session() as session:
                db_result = await session.execute(statement)
                orm_obj = db_result.scalars().one()
                return self.orm_to_grpc(orm_obj)

        return await self._try_execute(get_by_id_query, request, context)

    async def update(self, request, context):
        async def update_query():
            statement = select(self.orm_model).filter_by(id=request.id)
            async with get_session() as session:
                result = await session.execute(statement)
                orm_obj = result.scalars().one()

                update_data = self.grpc_to_orm(request)
                orm_obj = self.orm_to_orm_key(update_data, orm_obj)
                session.add(orm_obj)
                await session.flush()
                await session.refresh(orm_obj)

                logger.info(f"Updated object to {orm_obj}")
                return self.orm_to_grpc(orm_obj)

        return await self._try_execute(update_query, request, context)

    async def delete(self, request, context):
        async def delete_query():
            statement = select(self.orm_model).filter_by(id=request.id)
            async with get_session() as session:
                result = await session.execute(statement)
                orm_obj = result.scalars().one()

                await session.delete(orm_obj)
                await session.flush()

            return acronyms_pb2.Empty()

        return await self._try_execute(delete_query, request, context)

    async def _try_execute(self, func, request, context):
        try:
            opeartion = func.__name__.replace('_query', '').upper()
            logger.info(
                f"Executing {opeartion} for {self.orm_model.__name__}"
            )
            return await func()
        except DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(
                f'{self.orm_model.__name__} with ID {request.id} not found'
            )
            return acronyms_pb2.Empty()
        except Exception as e:
            logger.error(
                "Error occurred while executing "
                f"{opeartion} for {self.orm_model.__name__}: {e}"
            )
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal server error occurred: {e}")
            return acronyms_pb2.Empty()

    def set_dates(self, orm_acr, update=None, create=None):
        if update and hasattr(orm_acr, 'update_dt'):
            orm_acr.update_dt = update.date()

        if create and hasattr(orm_acr, 'create_dt'):
            orm_acr.create_dt = create

        return orm_acr

    def orm_to_grpc(self, acr):
        grpc_acr = self.grpc_model()
        for key, value in acr.__dict__.items():
            if value is None:
                continue
            if key.startswith('_'):
                continue

            if isinstance(value, datetime):
                setattr(grpc_acr, key, value)
            elif isinstance(value, date):
                setattr(grpc_acr, key, datetime.combine(value, datetime.min.time()))
            elif isinstance(value, Decimal):
                setattr(grpc_acr, key, int(value))
            else:
                setattr(grpc_acr, key, value)
        return grpc_acr

    def grpc_to_orm(self, acr):
        orm_acr = self.orm_model()
        for key, value in acr.ListFields():
            if key.name.startswith('_') or key.name.endswith('_dt'):
                continue
            setattr(orm_acr, key.name, value)

        return orm_acr

    def orm_to_orm_key(self, src, dest):

        for key in src.__dict__:

            if key == 'id' or key.startswith('_'):
                continue
            value = getattr(src, key)
            if value is None:
                continue
            setattr(dest, key, value)

        return dest
