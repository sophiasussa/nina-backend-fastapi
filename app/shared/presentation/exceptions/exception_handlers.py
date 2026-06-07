from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from app.modules.auth.domain.exceptions.auth_exceptions import AuthException
from app.modules.customer.domain.exceptions.customers_exceptions import (
    CustomerDomainError,
    CustomerNotFoundError,
    CustomerAlreadyExistsError,
    CustomerDocumentAlreadyExistsError,
    CustomerInactiveError,
)


async def auth_exception_handler(request: Request, exc: AuthException):
    return JSONResponse(status_code=401, content={"detail": str(exc)})


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=422, content={"detail": exc.errors()})


async def database_exception_handler(request: Request, exc: SQLAlchemyError):
    return JSONResponse(status_code=500, content={"detail": "Erro de banco de dados"})


async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"detail": "Erro interno do servidor"})


async def customer_exception_handler(request: Request, exc: CustomerDomainError):
    if isinstance(exc, CustomerNotFoundError):
        status_code = 404
    elif isinstance(exc, (CustomerAlreadyExistsError, CustomerDocumentAlreadyExistsError)):
        status_code = 409
    elif isinstance(exc, CustomerInactiveError):
        status_code = 422
    else:
        status_code = 400

    return JSONResponse(status_code=status_code, content={"detail": str(exc)})
