from sqlalchemy import Column, Identity, Integer
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, Identity(start=1), primary_key=True, name="ID")

    def to_dict(self):
        return {
            "id": self.id
        }

    def __str__(self):
        return f"BaseModel({self.to_dict()})"
