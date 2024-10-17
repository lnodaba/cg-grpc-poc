
from functools import wraps
import grpc
from services.proto import acronyms_pb2
from custom_logger import logger


def grpc_exception_handler_decorator(method):
    @wraps(method)
    async def wrapper(self, request, context):
        try:
            logger.info(f" {method.__name__} request: {request}")
            return await method(self, request)  # Call the method without context
        except Exception as e:
            if isinstance(e, ValueError):
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details(str(e))
                logger.info(f" {method.__name__} not found: {e}")
            else:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(f"Internal server error occurred: {e}")
                logger.error(f" {method.__name__} error: {e}")

            if self.repository is not None:
                await self.repository.rollback_transaction()

            return acronyms_pb2.Empty()

    return wrapper
