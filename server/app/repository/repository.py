

from dataclasses import dataclass
from turtle import update

from sqlalchemy import select, text
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

    # SQL queries as class constants for better readability
    _SET_ACTIVE_SQL = text("""
        UPDATE trainset
        SET is_active = CASE
            WHEN id = :trainset_id THEN TRUE
            ELSE FALSE
        END
        WHERE base_model_inst_id = :model_id
    """)

    _DUPLICATE_SQL = text("""
        INSERT INTO trainset (
            last_run,
            base_model_inst_id,
            new_model_inst_id,
            description,
            create_dt,
            version,
            created_by,
            is_active
        )
        SELECT
            last_run,
            base_model_inst_id,
            new_model_inst_id,
            description,
            create_dt,
            version,
            created_by,
            is_active
        FROM
            trainset
        WHERE
            id = :trainset_id
    """)

    async def set_active_by_id(self, model_id: int, trainset_id: int) -> Trainset:
        async with self.connection_manager.get_session() as session:
            await session.execute(
                self._SET_ACTIVE_SQL,
                {'trainset_id': trainset_id, 'model_id': model_id}
            )

            statement = select(Trainset).filter(Trainset.id == trainset_id)
            result = await session.execute(statement)
            return result.scalar()

    async def duplicate_by_id(self, trainset_id: int) -> Trainset:
        async with self.connection_manager.get_session() as session:
            await session.execute(
                self._DUPLICATE_SQL,
                {'trainset_id': trainset_id}
            )
            await session.commit()  # Commit to save the new trainset

            statement = select(Trainset).filter(Trainset.id == trainset_id+1)
            result = await session.execute(statement)
            return result.scalar()

    async def get_by_base_model_id(self, model_id: int) -> [Trainset]:
        async with self.connection_manager.get_session() as session:
            statement = select(
                        Trainset
                        ).filter(
                            Trainset.base_model_inst_id == model_id
                        ).order_by(Trainset.create_dt.desc())
            result = await session.execute(statement)
            return result.scalars().all()

@dataclass
class ModelRepository(BaseRepository[Model]):
    def __init__(self):
        super().__init__(Model)
