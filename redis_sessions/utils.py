from functools import wraps
try:  # Python 2.*
    from django.utils.encoding import force_unicode
except ImportError:  # Python 3.*
    from django.utils.encoding import force_text
    force_unicode = force_text
from redis_sessions import settings


def add_prefix(key):
    if not settings.SESSION_REDIS_PREFIX:
        return key
    return '%s:%s' % (
        settings.SESSION_REDIS_PREFIX,
        key
    )


def remove_prefix(key):
    if settings.SESSION_REDIS_PREFIX:
        key = key.replace(
            '%s:' % settings.SESSION_REDIS_PREFIX, '', 1
        )
    return key


def prefix(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        args = list(args)
        args[0] = add_prefix(args[0])
        return fn(*args, **kwargs)
    return wrapped
