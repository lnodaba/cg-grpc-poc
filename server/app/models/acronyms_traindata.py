from .base_model import BaseModel
from tortoise import fields


class AcronymTrainData(BaseModel):

    class Meta:
        table = "ACRONYMS_TRAINDATA"

    acronym_id = fields.IntField(null=True)
    provided_by = fields.CharField(max_length=20, null=True)
    generated_bytrainset_id = fields.IntField(null=True)
    text_en = fields.TextField(max_length=4000, null=True)
    text_fr = fields.CharField(max_length=4000, null=True)
    reason = fields.CharField(max_length=500, null=True)
    create_dt = fields.DateField(auto_now_add=True)
