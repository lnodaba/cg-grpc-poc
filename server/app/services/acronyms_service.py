from sqlalchemy import select
from models.trainset_contents import TrainsetContent
from services.base_service import BaseService
from services.trainset_service import TrainsetService
from services.trainset_contetns_service import TrainsetContentService
from services.proto import acronyms_pb2
import services.proto.acronyms_pb2_grpc as acronyms_pb2_grpc
from models.acronyms import Acronym
from sql_alchemy.connection import get_session
from custom_logger import logger


class AcronymService(
    acronyms_pb2_grpc.AcronymServiceServicer,
):
    def __init__(self):
        super().__init__()
        self.base_service = BaseService(
            Acronym,
            acronyms_pb2.Acronym,
            acronyms_pb2.AcronymList
        )

    async def create(self, request, context):
        return await self.base_service.create(request, context)

    async def get_all(self, request, context):
        return await self.base_service.get_all(request, context)

    async def get_by_id(self, request, context):
        return await self.base_service.get_by_id(request, context)

    async def update(self, request, context):
        return await self.base_service.update(request, context)

    async def delete(self, request, context):
        return await self.base_service.delete(request, context)

    async def add_to_trainset(
        self, request, context
    ):
        async def add_to_trainset_query():
            create_dto = self.base_service.grpc_to_orm(request.acronym)
            async with get_session() as session:
                session.add(create_dto)
                await session.flush()
                await session.refresh(create_dto)
                logger.info(f"Object {create_dto} saved")
  
            trainset_service = TrainsetService()

            await trainset_service.get_by_id(
                acronyms_pb2.IdRequest(id=request.trainset_id), context
            )

            trainset_contents_service = TrainsetContentService()

            new_trainset_content = acronyms_pb2.TrainsetContent(
                trainset_id=request.trainset_id,
                acronym_id=create_dto.id,
            )

            logger.info(f"Add acronym to trainset => trainset_content: {new_trainset_content} saved")

            await trainset_contents_service.create(
                new_trainset_content,
                context
            )

            return self.base_service.orm_to_grpc(create_dto)

        return await add_to_trainset_query()

    async def get_by_trainset_id(
        self, request, context
    ):
        async def get_acronym_by_trainset_id_query():
            try:
                async with get_session() as session:
                    statement = (
                        select(Acronym)
                        .select_from(Acronym)
                        .join(TrainsetContent, Acronym.id == TrainsetContent.acronym_id )  # Provide the join condition
                        .filter(TrainsetContent.trainset_id == request.id)
                    )
                    result = await session.execute(statement)
                    orm_obj_list = result.scalars().all()
                    dto_list = [
                        self.base_service.orm_to_grpc(orm_obj)
                        for orm_obj in orm_obj_list
                    ]
                    return self.base_service.grpc_model_list(list=dto_list)
            except Exception as e:
                logger.error(f"Error: {e}")
                return acronyms_pb2.Empty()
        return await get_acronym_by_trainset_id_query()
