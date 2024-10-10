

import grpc
from sqlalchemy import select
from cutom_logger import logger

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
        logger.info(f"Creating {self.orm_model.__name__}")
        create_dto = self.grpc_to_orm(request)

        try:
            async with get_session() as session:
                session.add(create_dto)
                await session.flush()
                await session.refresh(create_dto)
                logger.info(f"Object {create_dto} saved")
                return self.orm_to_grpc(create_dto)
        except Exception as e:
            logger.error(
                f"Error saving {self.orm_model.__name__} object: {e}"
            )
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(
                f"Error saving {self.orm_model.__name__} object."
            )
            return acronyms_pb2.Empty()

        return self.orm_to_grpc(create_dto)

    async def get_all(self, request, context):
        logger.info(f"Getting all {self.orm_model.__name__} objects")
        statement = select(self.orm_model)
        try:
            async with get_session() as session:
                result = await session.execute(statement)
                orm_obj_list = result.scalars().all()
                dto_list = [self.orm_to_grpc(orm_obj) for orm_obj in orm_obj_list]
                return self.grpc_model_list(list=dto_list)
        except Exception as e:
            logger.error(f"Error fetching {self.orm_model.__name__} objects: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal error occurred.")
            return acronyms_pb2.Empty()

    async def get_by_id(self, request, context):
        logger.info(
            f"Getting {self.orm_model.__name__} object with ID {request.id}"
        )
        statement = select(self.orm_model).filter_by(id=request.id)
        try:
            async with get_session() as session:
                result = await session.execute(statement)
                orm_obj = result.scalars().one()
                return self.orm_to_grpc(orm_obj)
        except DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f'Acronym with ID {request.id} not found')
            return acronyms_pb2.Empty()
        except Exception as e:
            logger.error(
                f"Error fetching {self.orm_model.__name__} object: {e}"
            )
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal error occurred.")
            return acronyms_pb2.Empty()

    async def update(self, request, context):
        logger.info(
            f"Updating {self.orm_model.__name__} object with ID {request.id}"
        )

        try:
            async with get_session() as session:
                statement = select(self.orm_model).filter_by(id=request.id)
                result = await session.execute(statement)
                orm_obj = result.scalars().one()

                update_data = self.grpc_to_orm(request)
                orm_obj = self.orm_to_orm_key(update_data, orm_obj)
                session.add(orm_obj)
                await session.flush()
                await session.refresh(orm_obj)

                logger.info(f"Updated object to {orm_obj}")
                return self.orm_to_grpc(orm_obj)
        except DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f'Acronym with ID {request.id} not found')
            return acronyms_pb2.Empty()
        except Exception as e:
            logger.error(
                f"Error updating {self.orm_model.__name__} object: {e}"
            )
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"{e}")
            return acronyms_pb2.Empty()

    async def delete(self, request, context):
        try:
            async with get_session() as session:
                statement = select(self.orm_model).filter_by(id=request.id)
                result = await session.execute(statement)
                orm_obj = result.scalars().one()

                await session.delete(orm_obj)
                await session.flush()

                logger.info(
                    f"{self.orm_model.__name__} " +
                    "object with ID {request.id} deleted"
                )
            return acronyms_pb2.Empty()
        except DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f'Acronym with ID {request.id} not found')
            return acronyms_pb2.Empty()
        except Exception as e:
            logger.error(
                f"Error deleting {self.orm_model.__name__} object: {e}"
            )
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal error occurred.")
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
