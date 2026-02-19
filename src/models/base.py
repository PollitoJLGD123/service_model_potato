from tortoise.models import Model
from tortoise import fields

class BaseModel(Model):
  id = fields.IntField(primary_key=True, generated=True)
  created_at = fields.DatetimeField(auto_now_add=True)
  updated_at = fields.DatetimeField(auto_now=True)
  deleted_at = fields.DatetimeField(null=True, default=None)

  class Meta:
    abstract = True