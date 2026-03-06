from fastapi import APIRouter, Request, HTTPException, Depends
from pydantic import BaseModel, Field
from datetime import date

from src.services import periodo_service
from src.helpers.response import success_response

router = APIRouter()


class PeriodoCreate(BaseModel):
    nombre: str = Field(..., max_length=255)
    descripcion: str | None = None
    fecha_inicio: date
    fecha_fin: date


@router.post("/periodos", status_code=201)
async def create_periodo(request: Request, body: PeriodoCreate):
    user_id = getattr(request.state, "user_id", None) or 1
    p = await periodo_service.create_periodo(
        user_id=user_id,
        nombre=body.nombre,
        descripcion=body.descripcion,
        fecha_inicio=body.fecha_inicio,
        fecha_fin=body.fecha_fin,
    )
    return success_response(periodo_service.periodo_to_dict(p), "Periodo creado", 201)


@router.get("/periodos", status_code=200)
async def list_periodos(request: Request):
    user_id = getattr(request.state, "user_id", None) or 1
    data = await periodo_service.list_periodos_by_user(user_id)
    return success_response(data, "Periodos obtenidos", 200)


@router.get("/periodos/{periodo_id}/predicciones", status_code=200)
async def get_predicciones_by_periodo(request: Request, periodo_id: int):
    # ensure user owns the periodo
    user_id = getattr(request.state, "user_id", None) or 1
    # simple check: fetch and compare
    from src.models.periodo import Periodo
    periodo = await Periodo.filter(id=periodo_id, usuario_id=user_id).first()
    if not periodo:
        raise HTTPException(status_code=404, detail="Periodo no encontrado")
    preds = await periodo_service.list_predicciones_by_periodo(periodo_id)
    return success_response(preds, "Predicciones de periodo", 200)
