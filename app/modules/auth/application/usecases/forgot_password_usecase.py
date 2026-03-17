from uuid import uuid4

from app.modules.auth.domain.value_objects.email_vo import Email
from redis import Redis

from app.modules.auth.domain.repositories.user_repository import UserRepository
from app.core.config import settings


class ForgotPasswordUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        redis: Redis,
    ):
        self.user_repository = user_repository
        self.redis = redis

    async def execute(self, email: Email):
        # 1. Busca usuário
        user = await self.user_repository.get_by_email(email)

        # 2. Segurança: não revela se existe ou não
        if not user:
            return

        # 3. Gera token
        token = uuid4().hex

        # 4. Salva no Redis (15 minutos)
        self.redis.setex(
            name=f"password_reset:{token}",
            time=settings.PASSWORD_RESET_TOKEN_EXPIRE_SECONDS,
            value=str(user.id.value),
        )

        # 5. Enviar email (por enquanto stub)
        reset_link = f"{settings.FRONTEND_URL}/reset-password?token={token}"

        # STUB TEMPORÁRIO (email depois)
        print(f"RESET LINK: {reset_link}")
       
        # send_email(
        #     to=user.email.value,
        #     subject="Recuperação de senha",
        #     body=f"Clique no link para redefinir sua senha: {reset_link}"
        # )

        return
