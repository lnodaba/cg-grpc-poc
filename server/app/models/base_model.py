from tortoise import fields

import uuid
from tortoise.models import Model


class BaseModel(Model):

    class Meta:
        abstract = True

    id = fields.IntField(pk=True, generated=True, autoincrement=True)
    
    def __str__(self):
        return str(self.__dict__)

    def store(self):
        self.refresh_from_db()
        self.save()
        return self