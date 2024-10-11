from sqlalchemy import Column, String, Date
from datetime import date

from models.base_model import BaseModel


class Acronym(BaseModel):
    __tablename__ = "ACRONYMS"

    acronym_en = Column(String(20), nullable=True, name="ACRONYM_EN")
    acronym_fr = Column(String(20), nullable=True, name="ACRONYM_FR")
    text_en = Column(String(100), nullable=True, name="TEXT_EN")
    text_fr = Column(String(100), nullable=True, name="TEXT_FR")
    create_dt = Column(Date, default=date.today, name="CREATE_DT")
    update_dt = Column(Date, onupdate=date.today, name="UPDATE_DT")

    def to_dict(self):
        return {
            **super().to_dict(),
            "acronym_en": self.acronym_en,
            "acronym_fr": self.acronym_fr,
            "text_en": self.text_en,
            "text_fr": self.text_fr,
            "create_dt": self.create_dt,
            "update_dt": self.update_dt
        }

    def __str__(self):
        return f"Acronym({self.to_dict()})"
