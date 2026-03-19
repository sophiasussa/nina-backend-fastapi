from app.core.config import settings
from app.modules.auth.domain.entities.user_entity import UserEntity
from app.modules.auth.domain.repositories.user_repository import UserRepository
from app.modules.auth.domain.value_objects.password_vo import Password
from app.modules.auth.presentation.schemas.current_user_response_schema import CurrentUserResponse
from app.modules.auth.presentation.schemas.login_response import LoginResponse
from app.shared.domain.value_objects.id_vo import Id
from app.modules.auth.application.services.jwt_service import JwtService
from app.modules.auth.application.services.google_token_verifier import GoogleTokenVerifier


class GoogleLoginUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        google_token_verifier: GoogleTokenVerifier,
        jwt_service: JwtService,
    ):
        self.user_repository = user_repository
        self.google_token_verifier = google_token_verifier
        self.jwt_service = jwt_service

    async def execute(self, id_token: str):
        # Valida token com Google
        email, name = await self.google_token_verifier.verify(id_token)

        """
        google_user deve conter:
        - email
        - name
        - google_id
        """

        # Busca usuário pelo email
        user = await self.user_repository.get_by_email(email)

        if not user:
            user = UserEntity(
                id = Id.new(),
                nome=name,
                email=email,
                password=Password.from_hashed(
                    "GOOGLE_EXTERNAL_AUTH_NO_PASSWORD_1234567890"
                ),
                is_active=True,
            )

            await self.user_repository.create(user)

        # Gera tokens
        access_token = self.jwt_service.create_access_token(
            subject=str(user.id.value)
        )

        refresh_token = self.jwt_service.create_refresh_token(
            subject=str(user.id.value)
        )

        # Retorno padrão de auth
        return LoginResponse(
            user=CurrentUserResponse.from_domain(user),
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="Bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )
