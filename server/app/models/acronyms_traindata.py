from sqlalchemy import Column, Integer, String, Text, Date
from datetime import date
from models.base_model import BaseModel


class AcronymTrainData(BaseModel):
    __tablename__ = "ACRONYMS_TRAINDATA"

    acronym_id = Column(Integer, nullable=True, name="ACRONYM_ID")
    provided_by = Column(String(20), nullable=True, name="PROVIDED_BY")
    generated_bytrainset_id = Column(Integer, nullable=True, name="GENERATED_BYTRAINSET_ID")
    text_en = Column(Text, nullable=True, name="TEXT_EN")
    text_fr = Column(String(4000), nullable=True, name="TEXT_FR")
    reason = Column(String(500), nullable=True, name="REASON")
    create_dt = Column(Date, default=date.today, name="CREATE_DT")

    def to_dict(self):
        return {
            **super().to_dict(),
            "acronym_id": self.acronym_id,
            "provided_by": self.provided_by,
            "generated_bytrainset_id": self.generated_bytrainset_id,
            "text_en": self.text_en,
            "text_fr": self.text_fr,
            "reason": self.reason,
            "create_dt": self.create_dt
        }

    def __str__(self):
        return f"AcronymTrainData({self.to_dict()})"
