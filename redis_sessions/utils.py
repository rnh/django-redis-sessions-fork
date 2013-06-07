from redis_sessions import settings
from redis_sessions.connection import redis_server
try:
    from django.utils.encoding import force_unicode
except ImportError:  # Python 3.*
    from django.utils.encoding import force_text as force_unicode


def expire(key):
    return redis_server.ttl(key)


def keys(pattern):
    return redis_server.keys(pattern)


def get(key):
    return redis_server.get(key)


def exists(key):
    return redis_server.exists(key)


def delete(key):
    return redis_server.delete(key)


def set(key, expire, data):
    redis_server.setex(key, expire, data)


def session_key(session_key):
    if not settings.SESSION_REDIS_PREFIX:
        return session_key
    return '%s:%s' % (
        settings.SESSION_REDIS_PREFIX,
        session_key
    )
