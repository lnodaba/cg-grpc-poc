import asyncio
from concurrent import futures
import grpc
from rodi import inject
from setup import build_provider
from config import NUM_WORKERS, PORT
from sql_alchemy.connection import init_db, close_pool
from services.proto import acronyms_pb2_grpc
from services.trainset_service import TrainsetService
from services.acronyms_service import AcronymService
from services.acronyms_traindata_service import AcronymTrainDataService
from services.trainset_contetns_service import TrainsetContentService
from services.model_service import ModelService
from custom_logger import logger


@inject()
async def run(
    acronym_service: AcronymService,
    acronym_traindata_service: AcronymTrainDataService,
    trainset_service: TrainsetService,
    trainset_content_service: TrainsetContentService,
    model_service: ModelService,
):

    server = grpc.aio.server(
        futures.ThreadPoolExecutor(max_workers=NUM_WORKERS)
    )
    acronyms_pb2_grpc.add_AcronymServiceServicer_to_server(
        acronym_service, server
    )

    acronyms_pb2_grpc.add_AcronymTrainDataServiceServicer_to_server(
        acronym_traindata_service, server
    )

    acronyms_pb2_grpc.add_TrainsetServiceServicer_to_server(
       trainset_service, server
    )

    acronyms_pb2_grpc.add_TrainsetContentServiceServicer_to_server(
        trainset_content_service, server
    )
    acronyms_pb2_grpc.add_ModelServiceServicer_to_server(
        model_service, server
    )

    server.add_insecure_port(f"[::]:{PORT}")
    logger.info(f"Starting server on port {PORT}")
    await server.start()
    await server.wait_for_termination()


async def main():
    try:
        logger.info("Starting server...")
        await init_db()

        provider = await build_provider()
        executor = provider.get_executor(run)
        await executor()
    except Exception as e:
        logger.error(f"Error starting server: {e}")
        await close_pool()

if __name__ == "__main__":
    asyncio.run(main())
