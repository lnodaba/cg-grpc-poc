

from dataclasses import dataclass

from sqlalchemy import select
from models.acronyms import Acronym
from models.acronyms_traindata import AcronymTrainData
from models.models import Model
from models.trainset import Trainset
from models.trainset_contents import TrainsetContent
from repository.base_respoitory import BaseRepository


@dataclass
class AcronymRepository(BaseRepository[Acronym]):
    def __init__(self):
        super().__init__(Acronym)

    async def find_by_trainset_id(self, trainset_id: int) -> list[Acronym]:
        async with self.connection_manager.get_session() as session:
            statement = (
                select(Acronym)
                .select_from(Acronym)
                .join(
                    TrainsetContent,
                    Acronym.id == TrainsetContent.acronym_id
                )
                .filter(TrainsetContent.trainset_id == trainset_id)
            )
            result = await session.execute(statement)
            return result.scalars().all()


@dataclass
class AcronymTrainDataRepository(BaseRepository[AcronymTrainData]):
    def __init__(self):
        super().__init__(AcronymTrainData)


@dataclass
class TrainsetContentRepository(BaseRepository[TrainsetContent]):
    def __init__(self):
        super().__init__(TrainsetContent)


@dataclass
class TrainsetRepository(BaseRepository[Trainset]):
    def __init__(self):
        super().__init__(Trainset)


@dataclass
class ModelRepository(BaseRepository[Model]):
    def __init__(self):
        super().__init__(Model)
