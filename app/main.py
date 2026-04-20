from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.core.config import settings
from app.shared.infrastructure.database.session import init_db
from app.shared.presentation.middlewares.auth_middleware import AuthMiddleware
from app.infra.redis.redis_client import RedisClient
from app.infra.redis.session_repository import RedisSessionRepository
from app.modules.auth.presentation.routes.auth_routes import router as auth_router

from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError

from app.shared.presentation.exceptions.exception_handlers import (
    auth_exception_handler,
    validation_exception_handler,
    database_exception_handler,
    generic_exception_handler,
)
from app.modules.auth.domain.exceptions.auth_exceptions import AuthException


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Iniciando aplicação...")

    init_db()
    redis = RedisClient.get_client()
    app.state.session_repository = RedisSessionRepository(redis)

    print("Banco e Redis prontos")
    yield
    print("Encerrando aplicação...")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan,
)

# HEALTH CHECK (rota raiz)
@app.get("/", tags=["health"])
def health_check():
    return {
        "status": "healthy",
        "service": "buskei-backend",
    }


# middleware
app.add_middleware(AuthMiddleware)

# REGISTRA AS ROTAS
app.include_router(auth_router, prefix="/api/v1")

# domínio
app.add_exception_handler(AuthException, auth_exception_handler)

# validação pydantic
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# banco
app.add_exception_handler(SQLAlchemyError, database_exception_handler)

# fallback
app.add_exception_handler(Exception, generic_exception_handler)
