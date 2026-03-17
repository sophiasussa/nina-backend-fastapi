from app.modules.auth.domain.value_objects.password_vo import Password
from app.modules.auth.domain.value_objects.plain_password_vo import PlainPassword
from app.shared.domain.value_objects.id_vo import Id
from redis import Redis
from app.modules.auth.domain.repositories.user_repository import UserRepository
from app.modules.auth.infrastructure.security.password_hasher import PasswordHasher


class ResetPasswordUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        redis: Redis,
        password_hasher: PasswordHasher,
    ):
        self.user_repository = user_repository
        self.redis = redis
        self.password_hasher = password_hasher

    async def execute(self, token: str, new_password: PlainPassword):
        redis_key = f"password_reset:{token}"

        user_id = self.redis.get(redis_key)
        if not user_id:
            raise ValueError("Token inválido ou expirado")

        user = await self.user_repository.get_by_id(Id(user_id))
        if not user:
            raise ValueError("Usuário não encontrado")

        hashed = self.password_hasher.hash(new_password.value)
        password = Password(hashed)

        await self.user_repository.update_password(
            user_id=Id(user_id),
            password=password,
        )

        self.redis.delete(redis_key)

        return user_id
