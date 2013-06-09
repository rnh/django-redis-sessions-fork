from redis_sessions import utils, connection


@utils.prefix
def expire(key):
    return connection.redis_server.ttl(key)


@utils.prefix
def keys(pattern):
    return connection.redis_server.keys(pattern)


@utils.prefix
def get(key, safe=True):
    value = connection.redis_server.get(key)
    if safe:
        value = utils.force_unicode(value)
    return value


@utils.prefix
def exists(key):
    return connection.redis_server.exists(key)


@utils.prefix
def delete(key):
    return connection.redis_server.delete(key)


@utils.prefix
def save(key, expire, data, safe=True):
    if safe:
        data = utils.force_unicode(data)
    connection.redis_server.setex(key, int(expire), data)
