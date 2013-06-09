import os
import time
from imp import reload
from nose.tools import eq_
from django.utils.importlib import import_module
from django.conf import settings as django_settings
from redis_sessions import settings as redis_sessions_settings
from redis_sessions import connection, utils


redis_session_module = import_module(django_settings.SESSION_ENGINE)
redis_session = redis_session_module.SessionStore()


def test_modify_and_keys():
    eq_(redis_session.modified, False)
    redis_session['test'] = 'test_me'
    eq_(redis_session.modified, True)
    eq_(redis_session['test'], 'test_me')


def test_save_and_delete():
    redis_session['key'] = 'value'
    redis_session.save()
    eq_(redis_session.exists(redis_session.session_key), True)
    redis_session.delete(redis_session.session_key)
    eq_(redis_session.exists(redis_session.session_key), False)


def test_flush():
    redis_session['key'] = 'another_value'
    redis_session.save()
    key = redis_session.session_key
    redis_session.flush()
    eq_(redis_session.exists(key), False)


def test_items():
    redis_session['item1'], redis_session['item2'] = 1, 2
    redis_session.save()
    # Python 3.* fix
    eq_(sorted(list(redis_session.items())), [('item1', 1), ('item2', 2)])


def test_expiry():
    redis_session.set_expiry(1)
    # Test if the expiry age is set correctly
    eq_(redis_session.get_expiry_age(), 1)
    redis_session['key'] = 'expiring_value'
    redis_session.save()
    key = redis_session.session_key
    eq_(redis_session.exists(key), True)
    time.sleep(2)
    eq_(redis_session.exists(key), False)


def test_save_and_load():
    redis_session.set_expiry(60)
    redis_session.setdefault('item_test', 8)
    redis_session.save()
    session_data = redis_session.load()
    eq_(session_data.get('item_test'), 8)


def test_redis_url_config():
    redis_sessions_settings.SESSION_REDIS_URL = 'redis://localhost:6379/0'

    reload(connection)

    redis_server = connection.redis_server

    host = redis_server.connection_pool.connection_kwargs.get('host')
    port = redis_server.connection_pool.connection_kwargs.get('port')
    db = redis_server.connection_pool.connection_kwargs.get('db')

    eq_(host, 'localhost')
    eq_(port, 6379)
    eq_(db, 0)


def test_redis_url_config_from_env():
    os.environ['MYREDIS_URL'] = 'redis://localhost:6379/0'

    reload(redis_sessions_settings)
    reload(connection)

    redis_server = connection.redis_server

    host = redis_server.connection_pool.connection_kwargs.get('host')
    port = redis_server.connection_pool.connection_kwargs.get('port')
    db = redis_server.connection_pool.connection_kwargs.get('db')

    eq_(host, 'localhost')
    eq_(port, 6379)
    eq_(db, 0)


def test_unix_socket():
    # Uncomment this in `redis.conf`:
    #
    # unixsocket /tmp/redis.sock
    # unixsocketperm 755
    redis_sessions_settings.SESSION_REDIS_URL = None
    redis_sessions_settings.SESSION_REDIS_UNIX_DOMAIN_SOCKET_PATH = \
        'unix:///tmp/redis.sock'

    reload(connection)

    redis_server = connection.redis_server

    path = redis_server.connection_pool.connection_kwargs.get('path')
    db = redis_server.connection_pool.connection_kwargs.get('db')

    eq_(path, redis_sessions_settings.SESSION_REDIS_UNIX_DOMAIN_SOCKET_PATH)
    eq_(db, 0)


def test_redis_prefix():
    eq_(
        utils.add_prefix('foo'),
        '%s:foo' % django_settings.SESSION_REDIS_PREFIX
    )

    eq_(
        'foo',
        utils.remove_prefix(utils.add_prefix('foo'))
    )

    redis_sessions_settings.SESSION_REDIS_PREFIX = ''

    eq_(utils.add_prefix('foo'), 'foo')

    eq_(
        'foo',
        utils.remove_prefix(utils.add_prefix('foo'))
    )
