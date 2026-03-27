from typing import Annotated
from fastapi import Depends, Header, HTTPException, status
from app.infra.redis.session_repository import RedisSessionRepository
from app.modules.auth.application.services.google_token_verifier import GoogleTokenVerifier
from app.modules.auth.application.services.jwt_service import JwtService
from app.modules.auth.application.usecases.google_login_usecase import GoogleLoginUseCase
from app.modules.auth.application.usecases.reset_password_usecase import ResetPasswordUseCase
from app.modules.auth.domain.repositories.session_repository import SessionRepository
from app.modules.auth.infrastructure.repositories.google_token_verifier_impl import GoogleTokenVerifierImpl
from app.modules.auth.infrastructure.repositories.jwt_service_impl import JwtServiceImpl
from redis import Redis
from sqlalchemy.orm import Session

from app.modules.auth.application.usecases.forgot_password_usecase import ForgotPasswordUseCase
from app.shared.infrastructure.database.session import get_db
from app.modules.auth.domain.entities.user_entity import UserEntity
from app.modules.auth.domain.repositories.user_repository import UserRepository
from app.modules.auth.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from app.modules.auth.infrastructure.security.jwt_handler import JWTHandler
from app.modules.auth.infrastructure.security.password_hasher import PasswordHasher
from app.modules.auth.application.usecases.login_usecase import LoginUseCase
from app.modules.auth.application.usecases.register_usecase import RegisterUseCase
from app.modules.auth.application.usecases.getcurrentuser_usecase import GetCurrentUserUseCase
from app.modules.auth.domain.exceptions.auth_exceptions import InvalidTokenException
from app.core.constants import TOKEN_TYPE_ACCESS

from app.infra.redis.dependencies import get_redis


# ============================================================
# Dependencies de Infraestrutura
# ============================================================

def get_password_hasher() -> PasswordHasher:
    """Dependency para obter PasswordHasher."""
    return PasswordHasher()


def get_jwt_handler() -> JWTHandler:
    """Dependency para obter JWTHandler."""
    return JWTHandler()


def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    """Dependency para obter UserRepository."""
    return UserRepositoryImpl(db)


# ============================================================
# Dependencies de UseCases
# ============================================================

def get_login_usecase(
    user_repository: UserRepository = Depends(get_user_repository),
    password_hasher: PasswordHasher = Depends(get_password_hasher),
) -> LoginUseCase:
    """Dependency para obter LoginUseCase."""
    return LoginUseCase(user_repository, password_hasher)


def get_register_usecase(
    user_repository: UserRepository = Depends(get_user_repository),
    password_hasher: PasswordHasher = Depends(get_password_hasher),
) -> RegisterUseCase:
    """Dependency para obter RegisterUseCase."""
    return RegisterUseCase(user_repository, password_hasher)


def get_current_user_usecase(
    user_repository: UserRepository = Depends(get_user_repository),
) -> GetCurrentUserUseCase:
    """Dependency para obter GetCurrentUserUseCase."""
    return GetCurrentUserUseCase(user_repository)


# ============================================================
# Dependencies de Autenticação
# ============================================================

async def get_token_from_header(
    authorization: Annotated[str | None, Header()] = None
) -> str:
    """
    Extrai token do header Authorization.
    
    Espera formato: "Bearer <token>"
    
    Raises:
        HTTPException: Se token não estiver presente ou formato inválido
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autenticação não fornecido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    parts = authorization.split()
    
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Formato de token inválido. Use: Bearer <token>",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return parts[1]


async def get_current_user(
    token: str = Depends(get_token_from_header),
    jwt_handler: JWTHandler = Depends(get_jwt_handler),
    get_user_uc: GetCurrentUserUseCase = Depends(get_current_user_usecase),
    redis: Redis = Depends(get_redis),
) -> UserEntity:

    try:
        # 1. Blacklist (logout)
        if redis.exists(f"blacklist:{token}"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token revogado",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # 2. Tipo do token
        if not jwt_handler.verify_token_type(token, TOKEN_TYPE_ACCESS):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token de acesso inválido",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # 3. User ID
        user_id = jwt_handler.get_user_id_from_token(token)

        # 4. Usuário
        user = await get_user_uc.execute(user_id)

        # 5. Ativo
        if not user.can_login():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuário inativo",
            )

        return user

    except HTTPException:
        raise

    except InvalidTokenException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )

    except Exception as e:
        print("Erro inesperado:", e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Não foi possível validar credenciais",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Type aliases para facilitar uso
CurrentUser = Annotated[UserEntity, Depends(get_current_user)]


def get_forgot_password_usecase(
    user_repository: UserRepository = Depends(get_user_repository),
    redis: Redis = Depends(get_redis),
) -> ForgotPasswordUseCase:
    return ForgotPasswordUseCase(
        user_repository=user_repository,
        redis=redis,
    )

def get_reset_password_usecase(
    user_repository: UserRepository = Depends(get_user_repository),
    redis: Redis = Depends(get_redis),
    password_hasher: PasswordHasher = Depends(get_password_hasher),
) -> ResetPasswordUseCase:
    return ResetPasswordUseCase(
        user_repository=user_repository,
        redis=redis,
        password_hasher=password_hasher,
    )

def get_jwt_service(
    jwt_handler: JWTHandler = Depends(get_jwt_handler),
) -> JwtService:
    return JwtServiceImpl(jwt_handler)

def get_google_token_verifier() -> GoogleTokenVerifier:
    return GoogleTokenVerifierImpl()

def get_google_login_usecase(
    user_repository: UserRepository = Depends(get_user_repository),
    google_token_verifier: GoogleTokenVerifier = Depends(get_google_token_verifier),
    jwt_service: JwtService = Depends(get_jwt_service),
) -> GoogleLoginUseCase:
    return GoogleLoginUseCase(
        user_repository=user_repository,
        google_token_verifier=google_token_verifier,
        jwt_service=jwt_service,
    )

def get_session_repository(
    redis: Redis = Depends(get_redis),
) -> SessionRepository:
    return RedisSessionRepository(redis)
