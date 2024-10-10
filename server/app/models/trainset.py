from models.base_model import BaseModel
from tortoise import fields


class Trainset(BaseModel):

    class Meta:
        table = "TRAINSET"

    last_run = fields.DateField(null=True)
    base_model_inst_id = fields.IntField(null=True)
    new_model_inst_id = fields.IntField(null=True)
    description = fields.CharField(max_length=1000, null=True)
    create_dt = fields.DateField(auto_now_add=True)
