from datetime import datetime, timezone
from redis import Redis

from app.modules.auth.domain.repositories.session_repository import SessionRepository


class RedisSessionRepository(SessionRepository):

    def __init__(self, redis: Redis):
        self.redis = redis

    def blacklist_access_token(self, token: str, expires_at: datetime) -> None:
        ttl = int((expires_at - datetime.utcnow()).total_seconds())

        if ttl > 0:
            self.redis.setex(
                name=f"blacklist:{token}",
                time=ttl,
                value="true",
            )

    def is_access_token_blacklisted(self, token: str) -> bool:
        return self.redis.exists(f"blacklist:{token}") == 1

    def store_refresh_token(self, jti: str, user_id: str, ttl_seconds: int) -> None:
        pipe = self.redis.pipeline()

        pipe.setex(
            name=f"refresh:{jti}",
            time=ttl_seconds,
            value=user_id,
        )

        pipe.sadd(f"user_sessions:{user_id}", jti)

        pipe.execute()

    def revoke_refresh_token(self, jti: str, user_id: str) -> None:
        pipe = self.redis.pipeline()

        pipe.delete(f"refresh:{jti}")
        pipe.srem(f"user_sessions:{user_id}", jti)

        pipe.execute()

    def is_refresh_token_valid(self, jti: str) -> bool:
        return self.redis.exists(f"refresh:{jti}") == 1

    def get_user_sessions(self, user_id: str):
        return self.redis.smembers(f"user_sessions:{user_id}")

    def revoke_all_sessions(self, user_id: str) -> None:
        jtis = self.redis.smembers(f"user_sessions:{user_id}")

        pipe = self.redis.pipeline()

        for jti in jtis:
            pipe.delete(f"refresh:{jti}")

        pipe.delete(f"user_sessions:{user_id}")

        pipe.execute()
    
    def is_refresh_token_used(self, jti: str) -> bool:
        return self.redis.exists(f"used_refresh:{jti}") == 1


    def mark_refresh_token_used(self, jti: str, ttl_seconds: int) -> None:
        self.redis.setex(f"used_refresh:{jti}", ttl_seconds, 1)
