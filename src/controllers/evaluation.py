from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Request
from src.models.classifier import classifier
from src.helpers.response import success_response
from src.helpers.auth import get_current_user_id
from src.services.roboflow_service import (
  roboflow_inference_service,
  validate_image_content_type,
)

router = APIRouter()

@router.post("/evaluate", status_code=200)
async def evaluate(file: UploadFile = File(...)):
  if not file.content_type or not file.content_type.startswith("image/"):
    raise HTTPException(status_code=400, detail="Invalid image format")

  img_bytes = await file.read()
  result = classifier.predict_all_models_bytes(img_bytes)
  return success_response(result, "Evaluation successful", status_code=200)


@router.post("/roboflow", status_code=200)
async def evaluate_roboflow(
  request: Request,
  file: UploadFile | None = File(None),
  image_url: str | None = Form(None),
):
  _ = get_current_user_id(request)

  if file and image_url:
    raise HTTPException(status_code=400, detail="Provide only one input: file or image_url")
  if not file and not image_url:
    raise HTTPException(status_code=400, detail="Provide either an image file or image_url")

  image_bytes: bytes | None = None
  if file:
    validate_image_content_type(file.content_type)
    image_bytes = await file.read()

  result = await roboflow_inference_service(image_bytes=image_bytes, image_url=image_url)

  message = "Roboflow inference successful"
  if not result.get("predictions"):
    message = "No hubo coincidencias"

  return success_response(result, message, status_code=200)