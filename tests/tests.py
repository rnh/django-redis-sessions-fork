import time
from nose.tools import eq_
from django.utils.importlib import import_module
from django.conf import settings


redis_session = import_module(settings.SESSION_ENGINE).SessionStore()


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


def test_with_redis_url_config():
    settings.SESSION_REDIS_URL = 'redis://localhost'

    redis_session = import_module(settings.SESSION_ENGINE).SessionStore()
    redis_server = redis_session.server

    host = redis_server.connection_pool.connection_kwargs.get('host')
    port = redis_server.connection_pool.connection_kwargs.get('port')
    db = redis_server.connection_pool.connection_kwargs.get('db')

    eq_(host, 'localhost')
    eq_(port, 6379)
    eq_(db, 0)


def test_with_unix_url_config():
    settings.SESSION_REDIS_URL = 'unix:///tmp/redis.sock'

    redis_session = import_module(settings.SESSION_ENGINE).SessionStore()
    redis_server = redis_session.server

    host = redis_server.connection_pool.connection_kwargs.get('host')
    port = redis_server.connection_pool.connection_kwargs.get('port')
    db = redis_server.connection_pool.connection_kwargs.get('db')

    eq_(host, 'localhost')
    eq_(port, 6379)
    eq_(db, 0)


# def test_load():
#     redis_session.set_expiry(60)
#     redis_session['item1'], redis_session['item2'] = 1,2
#     redis_session.save()
#     session_data = redis_session.server.get(redis_session.session_key)
#     expiry, data = int(session_data[:15]), session_data[15:]
