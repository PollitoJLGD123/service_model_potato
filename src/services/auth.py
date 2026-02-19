from src.lib.jwt import create_token, get_payload, get_user_id
from src.models.user import User
from fastapi import HTTPException
from src.lib.bycript import check_password

async def login_service(email: str, password: str):
  user = await User.get_or_none(email=email)

  if not user:
    raise HTTPException(status_code=401, detail="Invalid email or password")
  if not check_password(password, user.password):
    raise HTTPException(status_code=401, detail="Invalid email or password")
  
  token = create_token(user.id, user.email)
  
  return token

async def logout_service(token: str):
  payload = get_payload(token)
  user = await User.get_or_none(id=payload["user_id"])
  if not user:
    raise HTTPException(status_code=401, detail="Invalid token")
  return True

async def me_service(token: str):
  user_id = get_user_id(token)
  user = await User.get_or_none(id=user_id)
  if not user:
    raise HTTPException(status_code=401, detail="Invalid token")
  return {
    "id": user.id,
    "username": user.username,
    "email": user.email,
    "full_name": user.full_name,
  }
