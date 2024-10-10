from services.base_service import BaseService
from services.proto import acronyms_pb2, acronyms_pb2_grpc
from models.trainset_contents import TrainsetContent


class TrainsetContentService(
    acronyms_pb2_grpc.TrainsetContentService,
):

    def __init__(self):
        super().__init__()
        self.base_service = BaseService(
            TrainsetContent,
            acronyms_pb2.TrainsetContent,
            acronyms_pb2.TrainsetContentList
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
