

import grpc
from structlog import get_logger
from services.proto import acronyms_pb2
from datetime import date, datetime
from tortoise.exceptions import DoesNotExist
from decimal import Decimal
from tortoise.transactions import atomic
from tortoise.backends.oracle.executor import OracleExecutor
from tortoise.transactions import in_transaction

class BaseService:
    def __init__(self, OrmModel, GrpcModel, GrpcModelList):
        self.orm_model = OrmModel
        self.grpc_model = GrpcModel
        self.grpc_model_list = GrpcModelList
        self.logger = get_logger()

    async def create(self, request, context):
        self.logger.info(f"Creating {self.orm_model.__name__}")
        acr = self.grpc_to_orm(request)
        acr = self.set_dates(acr, create=datetime.now(), update=datetime.now())

        try:
            await acr.save()
            # await acr.refresh_from_db()
            self.logger.info(f"Object {acr} saved")
        except Exception as e:
            self.logger.error(
                f"Error saving {self.orm_model.__name__} object: {e}"
            )
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(
                f"Error saving {self.orm_model.__name__} object."
            )
            return acronyms_pb2.Empty()

        return self.orm_to_grpc(acr)

    async def get_all(self, request, context):
        self.logger.info(f"Getting all {self.orm_model.__name__} objects")
        acr_list = await self.orm_model.all()
        dto_list = [self.orm_to_grpc(acr) for acr in acr_list]
       
        return self.grpc_model_list(list=dto_list)

    async def get_by_id(self, request, context):
        self.logger.info(
            f"Getting {self.orm_model.__name__} object with ID {request.id}"
        )
        try:
            acr = await self.orm_model.get(id=request.id)
            return self.orm_to_grpc(acr)
        except DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f'Acronym with ID {request.id} not found')
            return acronyms_pb2.Empty()
        except Exception as e:
            self.logger.error(
                f"Error fetching {self.orm_model.__name__} object: {e}"
            )
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal error occurred.")
            return acronyms_pb2.Empty()

    async def update(self, request, context):
        self.logger.info(
            f"Updating {self.orm_model.__name__} object with ID {request.id}"
        )

        try:
            acr = self.grpc_to_orm(request)
            
            model = await self.orm_model.get(id=acr.id)
            model = self.orm_to_orm_key(acr, model)
            model = self.set_dates(model, update=datetime.now())
            self.logger.info(f"Update object to {acr}")
            
            await model.save()
            return self.orm_to_grpc(model)
        except DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f'Acronym with ID {request.id} not found')
            return acronyms_pb2.Empty()
        except Exception as e:
            self.logger.error(
                f"Error updating {self.orm_model.__name__} object: {e}"
            )   
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"{e}")
            return acronyms_pb2.Empty()

    async def delete(self, request, context):
        try:
            self.logger.info(f"Deleting {self.orm_model.__name__} object with ID {request.id}")

            acr = self.grpc_to_orm(request)
            acr = await self.orm_model.get(id=acr.id)

            await acr.delete()
            self.logger.info(
                f"{self.orm_model.__name__} " +
                "object with ID {request.id} deleted"
            )
            return acronyms_pb2.Empty()
        except DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f'Acronym with ID {request.id} not found')
            return acronyms_pb2.Empty()
        except Exception as e:
            self.logger.error(
                f"Error deleting {self.orm_model.__name__} object: {e}"
            )
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal error occurred.")
            return acronyms_pb2.Empty()

    def set_dates(self, orm_acr, update=None, create=None):
        if update and hasattr(orm_acr, 'update_dt'):
            orm_acr.update_dt = update

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

            if isinstance(value, date):
                if isinstance(value, datetime):
                    # It's already a datetime object
                    setattr(grpc_acr, key, value)
            elif isinstance(value, Decimal):
                # Convert Decimal fields to a Python int or float as needed
                setattr(grpc_acr, key, int(value))
            else:
                # Set other fields as they are
                setattr(grpc_acr, key, value)
        return grpc_acr

    def grpc_to_orm(self, acr):
        orm_acr = self.orm_model()
        for key, value in acr.ListFields():
            if key.name.startswith('_'):
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
