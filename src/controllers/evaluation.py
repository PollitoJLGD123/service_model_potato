from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Request
from src.models.classifier import classifier
from src.helpers.response import success_response
from src.services.roboflow_service import (
  roboflow_inference_service,
  validate_image_content_type,
)
from src.services.evaluation_service import (
  save_image_locally,
  create_prediccion_fase1,
  update_prediccion_fase2,
  list_predicciones_by_user,
  prediccion_to_dict,
)

router = APIRouter()


def _get_user_id(request: Request, default: int = 1) -> int:
  user_id = getattr(request.state, "user_id", None)
  return user_id if user_id else default


@router.post("/roboflow", status_code=200)
async def evaluate_roboflow(
  request: Request,
  file: UploadFile | None = File(None),
  image_url: str | None = Form(None),
):
  user_id = _get_user_id(request)
  
  if file and image_url:
    raise HTTPException(status_code=400, detail="Provide only one input: file or image_url")
  if not file and not image_url:
    raise HTTPException(status_code=400, detail="Provide either an image file or image_url")

  image_bytes: bytes | None = None
  saved_image_url: str | None = None

  if file:
    validate_image_content_type(file.content_type)
    image_bytes = await file.read()
    saved_image_url = save_image_locally(image_bytes, file.content_type, request)

  result = await roboflow_inference_service(image_bytes=image_bytes, image_url=image_url)

  await create_prediccion_fase1(
    user_id=user_id,
    imagen_url=saved_image_url or image_url or "",
    fase1_payload=result,
  )

  message = "Roboflow inference successful"
  if not result.get("predictions"):
    message = "No hubo coincidencias"

  return success_response(
    result,
    message,
    status_code=200,
  )


@router.post("/evaluate", status_code=200)
async def evaluate(
  request: Request,
  file: UploadFile = File(...),
):
  if not file.content_type or not file.content_type.startswith("image/"):
    raise HTTPException(status_code=400, detail="Invalid image format")

  user_id = _get_user_id(request)

  img_bytes = await file.read()
  result = classifier.predict_all_models_bytes(img_bytes)

  prediccion = await update_prediccion_fase2(user_id=user_id, fase2_payload=result)

  response_data = {
    "clasificacion": result,
  }
  if prediccion:
    response_data["prediccion"] = prediccion_to_dict(prediccion)

  return success_response(response_data, "Evaluation successful", status_code=200)


@router.get("/history", status_code=200)
async def get_evaluation_history(request: Request):
  user_id = _get_user_id(request)
  predicciones = await list_predicciones_by_user(user_id)
  return success_response(predicciones, "Historial de predicciones", status_code=200)
