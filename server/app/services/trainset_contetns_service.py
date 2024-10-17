from mapper.Mapper import TrainsetContentMapper
from repository.repository import TrainsetContentRepository
from services.base_service import grpc_exception_handler_decorator
from services.proto import acronyms_pb2_grpc


class TrainsetContentService(
    acronyms_pb2_grpc.TrainsetContentService
):

    def __init__(
        self,
        repository: TrainsetContentRepository,
        mapper: TrainsetContentMapper
    ):
        super().__init__()
        self.repository = repository
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
