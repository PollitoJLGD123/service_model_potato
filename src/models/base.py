from tortoise.models import Model
from tortoise import fields
from tortoise.fields.db_defaults import Now

class BaseModel(Model):
  id = fields.IntField(pk=True, generated=True)
  created_at = fields.DatetimeField(auto_now_add=True, null=True, default=Now())
  updated_at = fields.DatetimeField(auto_now=True, null=True, default=Now())
  deleted_at = fields.DatetimeField(null=True, default=Now())

  class Meta:
    abstract = True