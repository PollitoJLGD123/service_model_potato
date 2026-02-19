from fastapi import APIRouter
from src.services.auth import login_service, logout_service, me_service
from fastapi import Request, Response
from src.helpers.response import success_response

router = APIRouter()

@router.post("/login")
async def login(request: Request, response: Response):
  data = await request.json()
  token = await login_service(data["email"], data["password"])
  response.set_cookie(key="token_access", value=token, httponly=True, secure=True, samesite="strict")
  return success_response(None, "Login successful")

@router.post("/logout")
async def logout(request: Request, response: Response):
  token = request.cookies.get("token_access")
  await logout_service(token)
  response.delete_cookie(key="token_access")
  return success_response(None, "Logout successful")

@router.get("/me")
async def me(request: Request):
  token = request.cookies.get("token_access")
  user = await me_service(token)
  return success_response(user, "User fetched successfully")
