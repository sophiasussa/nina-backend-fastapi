from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError

from app.modules.auth.domain.exceptions.auth_exceptions import AuthException

import logging

logger = logging.getLogger(__name__)


async def auth_exception_handler(request: Request, exc: AuthException):
    """Handler para exceções de autenticação."""
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": exc.message},
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handler para erros de validação do Pydantic."""
    errors = []
    for error in exc.errors():
        errors.append({
            "field": ".".join(str(x) for x in error["loc"]),
            "message": error["msg"],
            "type": error["type"],
        })
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": "Erro de validação", "errors": errors},
    )


async def database_exception_handler(request: Request, exc: SQLAlchemyError):
    """Handler para erros de banco de dados."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Erro no banco de dados"},
    )


async def generic_exception_handler(request: Request, exc: Exception):
    """Handler genérico para exceções não tratadas."""
    logger.exception("Erro inesperado")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Erro interno do servidor"},
    )
