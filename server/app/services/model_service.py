from services.base_service import BaseService
from services.proto import acronyms_pb2
import services.proto.acronyms_pb2_grpc as acronyms_pb2_grpc
from models.models import Model


class ModelService(
    acronyms_pb2_grpc.ModelServiceServicer,
):
    def __init__(self):
        super().__init__()
        self.base_service = BaseService(
            Model,
            acronyms_pb2.Model,
            acronyms_pb2.ModelList
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
