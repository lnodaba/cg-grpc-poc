

from datetime import date, datetime
from decimal import Decimal
from typing import Generic, TypeVar

from models.acronyms import Acronym
from models.acronyms_traindata import AcronymTrainData
from models.models import Model
from models.trainset import Trainset
from models.trainset_contents import TrainsetContent
from services.proto import acronyms_pb2

GRPC_MODEL = TypeVar('GRPC_MODEL')
GRPC_MODEL_LIST = TypeVar('GRPC_MODEL_LIST')
ORM_MODEL = TypeVar('ORM_MODEL')


class BaseMapper(Generic[GRPC_MODEL, GRPC_MODEL_LIST, ORM_MODEL]):
    def __init__(self, orm_model, grpc_model,  grpc_model_list):
        self.grpc_model = grpc_model
        self.orm_model = orm_model
        self.grpc_model_list = grpc_model_list

    def orm_to_grpc(self, model: ORM_MODEL) -> GRPC_MODEL:
        grpc_model = self.grpc_model()
        for key, value in model.__dict__.items():
            if value is None:
                continue
            if key.startswith('_'):
                continue

            if isinstance(value, datetime):
                setattr(grpc_model, key, value)
            elif isinstance(value, date):
                setattr(grpc_model, key, datetime.combine(value, datetime.min.time()))
            elif isinstance(value, Decimal):
                setattr(grpc_model, key, int(value))
            else:
                setattr(grpc_model, key, value)
        return grpc_model

    def grpc_to_orm(self, model: GRPC_MODEL) -> ORM_MODEL:
        orm_model = self.orm_model()
        for key, value in model.ListFields():
            if key.name.startswith('_') or key.name.endswith('_dt'):
                continue
            setattr(orm_model, key.name, value)

        return orm_model

    def orm_to_grpc_list(self, models: list[ORM_MODEL]) -> list[GRPC_MODEL]:
        list = [self.orm_to_grpc(model) for model in models]
        return self.grpc_model_list(list=list)

    def orm_to_orm_key(self, src: ORM_MODEL, dest: ORM_MODEL) -> ORM_MODEL:

        for key in src.__dict__:

            if key == 'id' or key.startswith('_'):
                continue
            value = getattr(src, key)
            if value is None:
                continue
            setattr(dest, key, value)

        return dest

    def empty(self):
        return acronyms_pb2.Empty()


class AcronymMapper(BaseMapper):
    def __init__(self):
        super().__init__(
            Acronym,
            acronyms_pb2.Acronym,
            acronyms_pb2.AcronymList
        )

    def grpc_to_orm_acronym_with_transet_id(self, request):
        acr = self.grpc_to_orm(request.acronym)
        return acr, request.trainset_id


class AcronymTrandataMapper(BaseMapper):
    def __init__(self):
        super().__init__(
            AcronymTrainData,
            acronyms_pb2.AcronymTrainData,
            acronyms_pb2.AcronymTrainDataList
        )


class TrainsetContentMapper(BaseMapper):
    def __init__(self):
        super().__init__(
            TrainsetContent,
            acronyms_pb2.TrainsetContent,
            acronyms_pb2.TrainsetContentList
        )


class TrainsetMapper(BaseMapper):
    def __init__(self):
        super().__init__(
            Trainset,
            acronyms_pb2.Trainset,
            acronyms_pb2.TrainsetList
        )


class ModelMapper(BaseMapper):
    def __init__(self):
        super().__init__(Model, acronyms_pb2.Model, acronyms_pb2.ModelList)
