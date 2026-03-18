from redis import Redis
from fastapi import Depends

from app.infra.redis.redis_client import RedisClient
from app.infra.redis.session_repository import RedisSessionRepository
from app.modules.auth.domain.repositories.session_repository import SessionRepository


def get_redis() -> Redis:
    return RedisClient.get_client()


def get_session_repository_dep(
    redis: Redis = Depends(get_redis),
) -> SessionRepository:
    return RedisSessionRepository(redis)
