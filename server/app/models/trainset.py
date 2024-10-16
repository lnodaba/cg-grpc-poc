from sqlalchemy import Column, Integer, String, Date
from datetime import date

from models.base_model import BaseModel


class Trainset(BaseModel):
    __tablename__ = "TRAINSET"

    last_run = Column(Date, nullable=True, name="LAST_RUN")
    base_model_inst_id = Column(Integer, nullable=True, name="BASE_MODEL_INST_ID")
    new_model_inst_id = Column(Integer, nullable=True, name="NEW_MODEL_INST_ID")
    description = Column(String(1000), nullable=True, name="DESCRIPTION")
    create_dt = Column(Date, default=date.today, name="CREATE_DT")
    version = Column(String(20), nullable=True, name="VERSION")
    created_by = Column(String(100), nullable=True, name="CREATED_BY")

    def to_dict(self):
        return {
            **super().to_dict(),
            "last_run": self.last_run,
            "base_model_inst_id": self.base_model_inst_id,
            "new_model_inst_id": self.new_model_inst_id,
            "description": self.description,
            "create_dt": self.create_dt,
            "version": self.version,
            "created_by": self.created_by,
        }

    def __str__(self):
        return f"Trainset({self.to_dict()})"
