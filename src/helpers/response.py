from fastapi.responses import JSONResponse
from typing import Any

def success_response(data: Any, message: str = "Success") -> JSONResponse:
  return JSONResponse(content={"data": message, "status": "success", "message": message}, status_code=200)