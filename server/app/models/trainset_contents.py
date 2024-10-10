from models.base_model import BaseModel
from tortoise import fields


class TrainsetContent(BaseModel):

    class Meta:
        table = "TRAINSET_CONTENTS"

    trainset_id = fields.IntField(null=True)
    acronym_id = fields.IntField(null=True)
    traindata_id = fields.IntField(null=True)
    role = fields.CharField(max_length=20, null=True)
