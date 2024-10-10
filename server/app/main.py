import asyncio
from concurrent import futures
import grpc
from config import NUM_WORKERS
from sql_alchemy.connection import close_pool, init_db
from services.proto import acronyms_pb2_grpc
from services.trainset_service import TrainsetService
from services.acronyms_service import AcronymService
from services.acronyms_traindata_service import AcronymTrainDataService
from services.trainset_contetns_service import TrainsetContentService
from cutom_logger import logger


async def main():
    try:
        await init_db()
        server = grpc.aio.server(
            futures.ThreadPoolExecutor(max_workers=NUM_WORKERS)
        )
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
        logger.error("Server stopped")
    finally:
        logger.info("Database connections closed")
        logger.info("Server stopped")


if __name__ == "__main__":
    asyncio.run(main())
