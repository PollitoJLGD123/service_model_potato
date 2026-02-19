from fastapi import APIRouter, UploadFile, File, HTTPException
from src.models.classifier import classifier
from src.helpers.response import success_response

router = APIRouter()

@router.post("/evaluate", status_code=200)
async def evaluate(file: UploadFile = File(...)):
  if not file.content_type or not file.content_type.startswith("image/"):
    raise HTTPException(status_code=400, detail="Invalid image format")

  img_bytes = await file.read()
  result = classifier.predict_bytes(img_bytes)
  return success_response(result, "Evaluation successful", status_code=200)