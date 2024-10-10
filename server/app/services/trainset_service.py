from services.base_service import BaseService
from services.proto import acronyms_pb2_grpc
from models.trainset import Trainset
import services.proto.acronyms_pb2 as acronyms_pb2


class TrainsetService(
    acronyms_pb2_grpc.TrainsetServiceServicer,
):

    def __init__(self):
        super().__init__()
        self.base_service = BaseService(
            Trainset,
            acronyms_pb2.Trainset,
            acronyms_pb2.TrainsetList
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
