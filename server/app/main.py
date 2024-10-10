import asyncio
from concurrent import futures
import grpc
from tortoise import Tortoise

from services.proto import acronyms_pb2_grpc
from config import DATABASE_CONFIG

from structlog import get_logger

from services.trainset_service import TrainsetService
from services.acronyms_service import AcronymService
from services.acronyms_traindata_service import AcronymTrainDataService
from services.trainset_contetns_service import TrainsetContentService
import logging
logger = get_logger()
logging.basicConfig(level=logging.DEBUG)


async def main():
    try:

        await Tortoise.init(config=DATABASE_CONFIG)
        logger.info("Tortoise ORM initialized")

        logger.info("Database connection established")

        # await Tortoise.generate_schemas(safe=True)

        logger.info("Database and schemas generated")
# futures.ThreadPoolExecutor(max_workers=1)
        server = grpc.aio.server()
        acronyms_pb2_grpc.add_AcronymTrainDataServiceServicer_to_server(
            AcronymTrainDataService(), server
        )

        acronyms_pb2_grpc.add_AcronymServiceServicer_to_server(
            AcronymService(), server
        )

        acronyms_pb2_grpc.add_TrainsetContentServiceServicer_to_server(
            TrainsetContentService(), server
        )

        acronyms_pb2_grpc.add_TrainsetServiceServicer_to_server(
            TrainsetService(), server
        )

        server.add_insecure_port("[::]:50051")
        await server.start()
        logger.info("Server started on port 50051")
        await server.wait_for_termination()
        logger.info("Server terminated")
    except Exception as e:
        logger.error(f"Error: {e}")
        # traceback.print_exc()
        logger.error("Server stopped")
    finally:
        # Close all database connections
        await Tortoise.close_connections()
        logger.info("Database connections closed")
        logger.info("Server stopped")


if __name__ == "__main__":
    asyncio.run(main())
