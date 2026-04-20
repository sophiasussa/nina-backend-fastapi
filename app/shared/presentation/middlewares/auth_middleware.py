from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.shared.presentation.exempt_paths import EXEMPT_PATHS


from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.shared.presentation.exempt_paths import EXEMPT_PATHS

class AuthMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        # 1. rotas públicas
        if request.url.path in EXEMPT_PATHS:
            return await call_next(request)

        # 2. repositório de sessão
        session_repo = getattr(request.app.state, "session_repository", None)
        if session_repo is None:
            return JSONResponse(
                status_code=500,
                content={"detail": "Session repository não inicializado"},
            )

        # 3. Authorization obrigatório
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=401,
                content={"detail": "Token não informado"},
            )

        token = auth_header.split(" ")[1]

        # 4. token revogado
        if session_repo.is_access_token_blacklisted(token):
            return JSONResponse(
                status_code=401,
                content={"detail": "Token revogado"},
            )

        return await call_next(request)
