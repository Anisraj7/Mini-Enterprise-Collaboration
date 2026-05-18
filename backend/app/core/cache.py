import json
import logging
from functools import lru_cache
from typing import Any

from fastapi.encoders import jsonable_encoder

try:
    from redis import Redis
    from redis.exceptions import RedisError
except ImportError:
    Redis = None

    class RedisError(Exception):
        pass

from app.core.config import CACHE_DEFAULT_TTL_SECONDS, REDIS_URL

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def get_redis_client():
    if Redis is None:
        return None
    return Redis.from_url(REDIS_URL, decode_responses=True)


def _redis():
    try:
        client = get_redis_client()
        if client is None:
            return None
        client.ping()
        return client
    except RedisError as exc:
        logger.debug("Redis cache unavailable: %s", exc)
        return None


def cache_get(key: str) -> Any | None:
    client = _redis()
    if not client:
        return None

    try:
        value = client.get(key)
        if value is None:
            return None
        return json.loads(value)
    except (RedisError, json.JSONDecodeError) as exc:
        logger.debug("Redis cache read failed for %s: %s", key, exc)
        return None


def cache_set(key: str, value: Any, ttl_seconds: int = CACHE_DEFAULT_TTL_SECONDS) -> None:
    client = _redis()
    if not client:
        return

    try:
        payload = json.dumps(jsonable_encoder(value))
        client.setex(key, ttl_seconds, payload)
    except (RedisError, TypeError) as exc:
        logger.debug("Redis cache write failed for %s: %s", key, exc)


def cache_delete_pattern(pattern: str) -> None:
    client = _redis()
    if not client:
        return

    try:
        keys = list(client.scan_iter(match=pattern))
        if keys:
            client.delete(*keys)
    except RedisError as exc:
        logger.debug("Redis cache invalidation failed for %s: %s", pattern, exc)


def invalidate_read_caches() -> None:
    cache_delete_pattern("tasks:*")
    cache_delete_pattern("dashboard:*")
    cache_delete_pattern("kanban:*")
    cache_delete_pattern("users:*")
    cache_delete_pattern("notifications:*")
    cache_delete_pattern("comments:*")
    cache_delete_pattern("approvals:*")
    cache_delete_pattern("documents:*")
    cache_delete_pattern("activity:*")
    cache_delete_pattern("audit:*")
