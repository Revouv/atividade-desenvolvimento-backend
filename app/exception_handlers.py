from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.exceptions import DomainError
from app.responses import error_response


async def _handle_domain_error(_: Request, exc: DomainError):
    return error_response(exc.message, status_code=exc.status_code)


async def _handle_validation_error(_: Request, exc: RequestValidationError):
    return error_response(
        "Dados inválidos", status_code=422, data=exc.errors()
    )


async def _handle_http_exception(_: Request, exc: StarletteHTTPException):
    return error_response(str(exc.detail), status_code=exc.status_code)


async def _handle_unexpected_error(_: Request, exc: Exception):
    return error_response("Erro interno no servidor", status_code=500)


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(DomainError, _handle_domain_error)
    app.add_exception_handler(RequestValidationError, _handle_validation_error)
    app.add_exception_handler(StarletteHTTPException, _handle_http_exception)
    app.add_exception_handler(Exception, _handle_unexpected_error)
