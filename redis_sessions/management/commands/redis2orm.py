import datetime
from binascii import Error
from django.contrib.sessions.backends.db import SessionStore
from django.core.management.base import NoArgsCommand
from django.utils import timezone
from django.contrib.sessions.models import Session
from redis_sessions import settings, utils


class Command(NoArgsCommand):
    help = 'copy django orm sessions to redis'

    def handle_noargs(self, **options):
        if settings.SESSION_REDIS_PREFIX:
            pattern = '%s:*' % (
                settings.SESSION_REDIS_PREFIX,
            )
        else:
            pattern = '*'

        for key in utils.keys(pattern):
            value = utils.get(key)

            if value:
                value = utils.force_unicode(value)

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
