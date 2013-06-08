from functools import wraps
try:  # Python 2.*
    from django.utils.encoding import force_unicode
except ImportError:  # Python 3.*
    from django.utils.encoding import force_text
    force_unicode = force_text
from redis_sessions import settings


def redis_key(key):
    if not settings.SESSION_REDIS_PREFIX:
        return key
    return '%s:%s' % (
        settings.SESSION_REDIS_PREFIX,
        key
    )


def prefix(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        args = list(args)
        args[0] = redis_key(args[0])
        return fn(*args, **kwargs)
    return wrapped


def keys_pattern():
    if settings.SESSION_REDIS_PREFIX:
        pattern = '%s:*' % (
            settings.SESSION_REDIS_PREFIX,
        )
    else:
        pattern = '*'
    return pattern
