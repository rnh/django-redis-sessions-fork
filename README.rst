django-redis-sessions-fork
==========================

:info: Redis Session Backend For Django

.. image:: https://api.travis-ci.org/hellysmile/django-redis-sessions-fork.png
    :target: https://travis-ci.org/hellysmile/django-redis-sessions-fork


installation
------------

run ``pip install django-redis-sessions-fork`` or alternatively
download the tarball and run ``python setup.py install``

set ``redis_sessions.session`` as your session engine, like so::

    SESSION_ENGINE = 'redis_sessions.session'

optional settings::

    SESSION_REDIS_HOST = 'localhost'
    SESSION_REDIS_PORT = 6379
    SESSION_REDIS_DB = 0
    SESSION_REDIS_PASSWORD = 'password'
    SESSION_REDIS_PREFIX = 'session'

    # if you prefer domain socket connection
    # you can just add this line instead of SESSION_REDIS_HOST and SESSION_REDIS_PORT

    SESSION_REDIS_UNIX_DOMAIN_SOCKET_PATH = '/var/run/redis/redis.sock'

that's it

see: `django-redis-sessions-fork <http://pypi.python.org/pypi/django-redis-sessions-fork>`_ on pypi

tests::

    pip install tox
    tox
