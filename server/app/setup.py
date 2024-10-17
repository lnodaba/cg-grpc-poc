from rodi import Container

from repository.connection_manager import ConnectionManager
from mapper.Mapper import (
    AcronymMapper,
    AcronymTrandataMapper,
    ModelMapper,
    TrainsetContentMapper,
    TrainsetMapper
)
from repository.repository import (
    AcronymRepository,
    AcronymTrainDataRepository,
    ModelRepository,
    TrainsetContentRepository,
    TrainsetRepository
)
from services.acronyms_service import AcronymService
from services.acronyms_traindata_service import AcronymTrainDataService
from services.model_service import ModelService
from services.trainset_contetns_service import TrainsetContentService
from services.trainset_service import TrainsetService


async def build_provider() -> Container:
    container = Container()

    # mapper
    container.add_singleton(AcronymMapper)
    container.add_singleton(AcronymTrandataMapper)
    container.add_singleton(TrainsetContentMapper)
    container.add_singleton(TrainsetMapper)
    container.add_singleton(ModelMapper)

    # connection manager
    container.add_singleton(ConnectionManager)

    # repository
    container.add_singleton(AcronymRepository)
    container.add_singleton(AcronymTrainDataRepository)
    container.add_singleton(TrainsetContentRepository)
    container.add_singleton(TrainsetRepository)
    container.add_singleton(ModelRepository)

    # service
    container.add_singleton(AcronymService)
    container.add_singleton(AcronymTrainDataService)
    container.add_singleton(TrainsetContentService)
    container.add_singleton(TrainsetService)
    container.add_singleton(ModelService)

    return container.build_provider()
