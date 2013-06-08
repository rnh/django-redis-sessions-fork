import datetime
from binascii import Error
from django.contrib.sessions.backends.db import SessionStore
from django.core.management.base import NoArgsCommand
from django.utils import timezone
from django.contrib.sessions.models import Session
from redis_sessions import settings, utils, backend


class Command(NoArgsCommand):
    help = 'copy redis sessions to django orm'

    def handle_noargs(self, **options):
        keys = utils.keys(utils.keys_pattern())
        for key in keys:
            value = backend.get(key)

            if value:
                try:
                    SessionStore().decode(value)

                    now = timezone.now()

                    expire = now + datetime.timedelta(
                        seconds=utils.expire(key)
                    )

                    if settings.SESSION_REDIS_PREFIX:
                        key = key.replace(
                            settings.SESSION_REDIS_PREFIX, '', 1
                        )

                    Session(
                        session_key=key,
                        session_data=value,
                        expire_date=expire
                    ).save()

                except Error:
                    pass
