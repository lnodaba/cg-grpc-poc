from models.base_model import BaseModel
from tortoise import fields


class Acronym(BaseModel):

    class Meta:
        table = "ACRONYMS"

    acronym_en = fields.CharField(max_length=20, null=True)
    acronym_fr = fields.CharField(max_length=20, null=True)
    text_en = fields.CharField(max_length=100, null=True)
    text_fr = fields.CharField(max_length=100, null=True)
    create_dt = fields.DateField(auto_now_add=True)
    update_dt = fields.DateField(auto_now=True)
