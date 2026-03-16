from fastapi import HTTPException, status
from redis import Redis


def rate_limit(
    redis: Redis,
    key: str,
    limit: int,
    window_seconds: int,
):
    pipe = redis.pipeline()

    pipe.incr(key)
    pipe.ttl(key)

    count, ttl = pipe.execute()

    # primeira vez que a chave aparece
    if ttl in (-1, -2):
        redis.expire(key, window_seconds)

    if count > limit:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Muitas tentativas. Tente novamente mais tarde.",
        )
