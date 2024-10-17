from mapper.Mapper import AcronymMapper
from repository.repository import (
    AcronymRepository,
    TrainsetContentRepository,
    TrainsetRepository
)
from models.trainset_contents import TrainsetContent
from services.base_service import grpc_exception_handler_decorator

import services.proto.acronyms_pb2_grpc as acronyms_pb2_grpc


class AcronymService(
    acronyms_pb2_grpc.AcronymServiceServicer
):
    def __init__(
        self,
        repository: AcronymRepository,
        trainset_repository: TrainsetRepository,
        trainset_content_repository: TrainsetContentRepository,
        mapper: AcronymMapper
    ):
        super().__init__()
        self.repository = repository
        self.trainset_repository = trainset_repository
        self.trainset_content_repository = trainset_content_repository
        self.mapper = mapper

    @grpc_exception_handler_decorator
    async def create(self, request):
        model = self.mapper.grpc_to_orm(request)
        model = await self.repository.create(model)
        return self.mapper.orm_to_grpc(model)

    @grpc_exception_handler_decorator
    async def get_all(self, request):
        models = await self.repository.get_all()
        return self.mapper.orm_to_grpc_list(models)

    @grpc_exception_handler_decorator
    async def get_by_id(self, request):
        model = await self.repository.get_by_id(request.id)
        return self.mapper.orm_to_grpc(model)

    @grpc_exception_handler_decorator
    async def update(self, request):
        model = self.mapper.grpc_to_orm(request)

        is_exist = await self.repository.get_by_id(request.id)
        if not is_exist:
            return ValueError(f"Acronym with id {request.id} not found")

        model = await self.repository.update(request.id, model)
        return self.mapper.orm_to_grpc(model)

    @grpc_exception_handler_decorator
    async def delete(self, request):
        await self.repository.delete(request.id)
        return self.mapper.empty()

    @grpc_exception_handler_decorator
    async def add_to_trainset(
        self, request
    ):
        acronym, trainset_id = self.mapper.grpc_to_orm_acronym_with_transet_id(
            request
        )

        # await self.repository.start_transaction()
        found_acronym = await self.repository.get_by_id(request.acronym.id)
        if not found_acronym:
            acronym = await self.repository.create(acronym)
        else:
            acronym = found_acronym

        trainset = await self.trainset_repository.get_by_id(trainset_id)

        if not trainset:
            raise ValueError(f"Trainset with id {trainset_id} not found")

        trainset_content = TrainsetContent(
            acronym_id=acronym.id,
            trainset_id=trainset.id,
        )
        await self.trainset_content_repository.create(trainset_content)
        # await self.repository.end_transaction()
        return self.mapper.orm_to_grpc(acronym)

    @grpc_exception_handler_decorator
    async def get_by_trainset_id(self, request):
        models = await self.repository.find_by_trainset_id(request.id)
        return self.mapper.orm_to_grpc_list(models)
