try:
    import ujson

    class UjsonSerializer(object):
        def dumps(self, obj):
            return ujson.dumps(obj)

        def loads(self, data):
            return ujson.loads(data)
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