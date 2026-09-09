from typing import Any

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


def _build_body(success: bool, message: str, data: Any) -> dict[str, Any]:
    return {"success": success, "message": message, "data": jsonable_encoder(data)}


def success_response(
    message: str, data: Any = None, status_code: int = 200
) -> JSONResponse:
    """Resposta de sucesso já serializada."""
    return JSONResponse(
        status_code=status_code, content=_build_body(True, message, data)
    )


def error_response(message: str, status_code: int, data: Any = None) -> JSONResponse:
    """Resposta de erro já serializada."""
    return JSONResponse(
        status_code=status_code, content=_build_body(False, message, data)
    )
