from fastapi.responses import JSONResponse
from typing import Any

def success_response(data: Any, message: str = "Success", status_code: int = 200) -> JSONResponse:
  return JSONResponse(content={"data": data, "status": "success", "message": message}, status_code=status_code)