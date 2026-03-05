from tortoise import fields

from src.models.base import BaseModel


class Prediccion(BaseModel):
    surco = fields.ForeignKeyField("models.Surco", related_name="predicciones", on_delete=fields.CASCADE)
    usuario = fields.ForeignKeyField("models.User", related_name="predicciones", on_delete=fields.CASCADE)
    imagen_url = fields.TextField()
    fase1_resumen = fields.JSONField()
    fase1_payload = fields.JSONField()
    fase2_resumen = fields.JSONField()
    fase2_payload = fields.JSONField()
    fecha = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "predicciones"
