import redis
from redis_sessions import settings


if not settings.SESSION_REDIS_URL is None:
    redis_server = redis.StrictRedis.from_url(settings.SESSION_REDIS_URL)
elif settings.SESSION_REDIS_UNIX_DOMAIN_SOCKET_PATH is None:
    redis_server = redis.StrictRedis(
        host=settings.SESSION_REDIS_HOST,
        port=settings.SESSION_REDIS_PORT,
        db=settings.SESSION_REDIS_DB,
        password=settings.SESSION_REDIS_PASSWORD
    )
else:
    redis_server = redis.StrictRedis(
        unix_socket_path=settings.SESSION_REDIS_UNIX_DOMAIN_SOCKET_PATH,
        db=settings.SESSION_REDIS_DB,
        password=settings.SESSION_REDIS_PASSWORD
    )
