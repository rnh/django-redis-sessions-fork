from .settings import SESSION_REDIS_JSON_ENCODING

try:
    import ujson

    class UjsonSerializer(object):
        def dumps(self, obj):
            return ujson.dumps(obj).encode(SESSION_REDIS_JSON_ENCODING)

        def loads(self, data):
            return ujson.loads(data.decode(SESSION_REDIS_JSON_ENCODING))
except ImportError:
    pass


try:
    import msgpack

    class MsgpackSerializer(object):
        def dumps(self, obj):
            return msgpack.packb(obj)

        def loads(self, data):
            return msgpack.unpackb(data)
except ImportError:
    pass


try:
    import umsgpack

    class UmsgpackSerializer(object):
        def dumps(self, obj):
            return umsgpack.packb(obj)

        def loads(self, data):
            return umsgpack.unpackb(data)
except ImportError:
    pass
