import redis
from redis import Redis

from app.core.redis_settings import redis_settings


class RedisClient:
    _client: Redis | None = None

    @classmethod
    def get_client(cls) -> Redis:
        if cls._client is None:
            cls._client = redis.Redis(
                host=redis_settings.host,
                port=redis_settings.port,
                db=redis_settings.db,
                password=redis_settings.password,
                decode_responses=True,
            )

        return cls._client
