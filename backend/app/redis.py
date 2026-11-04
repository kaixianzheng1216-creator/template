from redis import Redis

from app.config import settings

redis_client: Redis = Redis.from_url(
    settings.REDIS_URL.get_secret_value(),
    decode_responses=True,
    socket_connect_timeout=2,
    socket_timeout=2,
)
