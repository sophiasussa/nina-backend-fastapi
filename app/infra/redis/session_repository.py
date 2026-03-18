from datetime import datetime, timezone
from redis import Redis

from app.modules.auth.domain.repositories.session_repository import SessionRepository


class RedisSessionRepository(SessionRepository):

    def __init__(self, redis: Redis):
        self._redis = redis

    def blacklist_access_token(self, token: str, expires_at: datetime) -> None:
        now = datetime.now(timezone.utc)
        ttl = int((expires_at - now).total_seconds())

        if ttl > 0:
            self._redis.setex(f"blacklist:{token}", ttl, "true")

    def is_access_token_blacklisted(self, token: str) -> bool:
        return self._redis.exists(f"blacklist:{token}") == 1

    def store_refresh_token(self, jti: str, user_id: str, ttl_seconds: int) -> None:
        self._redis.setex(
            name=f"refresh:{jti}",
            time=ttl_seconds,
            value=user_id,
        )

    def revoke_refresh_token(self, jti: str) -> None:
        self._redis.delete(f"refresh:{jti}")

    def is_refresh_token_valid(self, jti: str) -> bool:
        return self._redis.exists(f"refresh:{jti}") == 1
