from sqlalchemy import Column, Float, Integer, String, Date
from models.base_model import BaseModel


class Model(BaseModel):

    __tablename__ = "MODELS"

    name = Column(String(100), nullable=True, name="NAME")
    version = Column(String(20), nullable=True, name="VERSION")
    date = Column(Date, name="DATE")
    checkpoint = Column(Integer, nullable=True, name="CHECKPOINT")
    score = Column(Float, nullable=True, name="SCORE")
    department = Column(String(100), nullable=True, name="DEPARTMENT")
    status = Column(String(100), nullable=True, name="STATUS")

    def to_dict(self):
        return {
            **super().to_dict(),
            "name": self.name,
            "version": self.version,
            "date": self.date,
            "checkpoint": self.checkpoint,
            "score": self.score,
            "department": self.department,
            "status": self.status,
        }

    def __str__(self):
        return f"Model({self.to_dict()})"
