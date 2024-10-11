from sqlalchemy import Column, Integer, String

from models.base_model import BaseModel


class TrainsetContent(BaseModel):
    __tablename__ = "TRAINSET_CONTENTS"

    trainset_id = Column(Integer, nullable=True, name="TRAINSET_ID")
    acronym_id = Column(Integer, nullable=True, name="ACRONYM_ID")
    traindata_id = Column(Integer, nullable=True, name="TRAINDATA_ID")
    role = Column(String(20), nullable=True, name="ROLE")

    def to_dict(self):
        return {
            **super().to_dict(),
            "trainset_id": self.trainset_id,
            "acronym_id": self.acronym_id,
            "traindata_id": self.traindata_id,
            "role": self.role
        }

    def __str__(self):
        return f"TrainsetContent({self.to_dict()})"
