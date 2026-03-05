from fastapi import APIRouter, File, Form, Request, UploadFile

from src.helpers.auth import get_current_user_id
from src.helpers.response import success_response
from src.schemas.cultivo import LoteCreate, ModuloCreate, SurcoCreate
from src.services.cultivo import (
    create_lote,
    create_modulo,
    create_surco,
    evaluar_y_guardar_prediccion,
    get_modulo_detail,
    get_prediccion_detail,
    list_lotes,
    list_modulos,
    list_predicciones,
    list_surcos,
)
from src.services.roboflow_service import validate_image_content_type

router = APIRouter()


@router.get("", status_code=200)
async def obtener_modulos(request: Request):
    user_id = get_current_user_id(request)
    modulos = await list_modulos(user_id)
    return success_response(modulos, "Modulos fetched successfully", status_code=200)


@router.post("", status_code=201)
async def crear_modulo(body: ModuloCreate, request: Request):
    user_id = get_current_user_id(request)
    modulo = await create_modulo(user_id, body.nombre, body.descripcion)
    return success_response(modulo, "Modulo created successfully", status_code=201)


@router.get("/{modulo_id}", status_code=200)
async def obtener_modulo(modulo_id: int, request: Request):
    user_id = get_current_user_id(request)
    modulo = await get_modulo_detail(user_id, modulo_id)
    return success_response(modulo, "Modulo fetched successfully", status_code=200)


@router.get("/{modulo_id}/lotes", status_code=200)
async def obtener_lotes(modulo_id: int, request: Request):
    user_id = get_current_user_id(request)
    lotes = await list_lotes(user_id, modulo_id)
    return success_response(lotes, "Lotes fetched successfully", status_code=200)


@router.post("/{modulo_id}/lotes", status_code=201)
async def crear_lote(modulo_id: int, body: LoteCreate, request: Request):
    user_id = get_current_user_id(request)
    lote = await create_lote(user_id, modulo_id, body.identificador, body.descripcion)
    return success_response(lote, "Lote created successfully", status_code=201)


@router.get("/{modulo_id}/lotes/{lote_id}/surcos", status_code=200)
async def obtener_surcos(modulo_id: int, lote_id: int, request: Request):
    user_id = get_current_user_id(request)
    surcos = await list_surcos(user_id, modulo_id, lote_id)
    return success_response(surcos, "Surcos fetched successfully", status_code=200)


@router.post("/{modulo_id}/lotes/{lote_id}/surcos", status_code=201)
async def crear_surco(modulo_id: int, lote_id: int, body: SurcoCreate, request: Request):
    user_id = get_current_user_id(request)
    surco = await create_surco(user_id, modulo_id, lote_id, body.numero, body.descripcion)
    return success_response(surco, "Surco created successfully", status_code=201)


@router.get("/{modulo_id}/lotes/{lote_id}/surcos/{surco_id}/predicciones", status_code=200)
async def obtener_predicciones(modulo_id: int, lote_id: int, surco_id: int, request: Request):
    user_id = get_current_user_id(request)
    predicciones = await list_predicciones(user_id, modulo_id, lote_id, surco_id)
    return success_response(predicciones, "Predicciones fetched successfully", status_code=200)


@router.get("/{modulo_id}/lotes/{lote_id}/surcos/{surco_id}/predicciones/{prediccion_id}", status_code=200)
async def obtener_prediccion(
    modulo_id: int,
    lote_id: int,
    surco_id: int,
    prediccion_id: int,
    request: Request,
):
    user_id = get_current_user_id(request)
    prediccion = await get_prediccion_detail(user_id, modulo_id, lote_id, surco_id, prediccion_id)
    return success_response(prediccion, "Prediccion fetched successfully", status_code=200)


@router.post("/{modulo_id}/lotes/{lote_id}/surcos/{surco_id}/predicciones/evaluar", status_code=201)
async def evaluar_surco(
    modulo_id: int,
    lote_id: int,
    surco_id: int,
    request: Request,
    file: UploadFile | None = File(None),
    image_url: str | None = Form(None),
):
    user_id = get_current_user_id(request)

    image_bytes: bytes | None = None
    if file:
        validate_image_content_type(file.content_type)
        image_bytes = await file.read()

    prediccion = await evaluar_y_guardar_prediccion(
        user_id=user_id,
        modulo_id=modulo_id,
        lote_id=lote_id,
        surco_id=surco_id,
        image_bytes=image_bytes,
        image_url=image_url,
        filename=file.filename if file else None,
    )

    return success_response(prediccion, "Prediccion created successfully", status_code=201)
