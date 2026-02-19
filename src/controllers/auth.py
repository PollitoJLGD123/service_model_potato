from fastapi import APIRouter, Request, Response, HTTPException
from src.services.auth import login_service, logout_service, me_service
from src.helpers.response import success_response
from src.schemas.auth import LoginRequest
from src.config import get_config
from datetime import timedelta

config = get_config()
router = APIRouter()

@router.post("/login", status_code=200)
async def login(body: LoginRequest, response: Response):
  token = await login_service(body.email, body.password)
  return success_response({"token": token}, "Login successful", status_code=200)

@router.post("/logout", status_code=200)
async def logout(request: Request, response: Response):
  token = request.cookies.get(config.NAME_COOKIE)
  if token:
    await logout_service(token)
  return success_response(None, "Logout successful", status_code=200)

@router.get("/me", status_code=200)
async def me(request: Request):
  token = request.cookies.get(config.NAME_COOKIE)
  if not token:
    raise HTTPException(status_code=401, detail="No token provided")
  user = await me_service(token)
  return success_response(user, "User fetched successfully", status_code=200)
