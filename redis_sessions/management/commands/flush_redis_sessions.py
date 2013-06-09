from binascii import Error
from django.core.management.base import NoArgsCommand
from django.contrib.sessions.backends.db import SessionStore
from redis_sessions import backend


class Command(NoArgsCommand):
    help = 'flush all redis sessions'

    def handle_noargs(self, **options):
        session_keys = backend.keys('*')

        for session_key in session_keys:
            session_data = backend.get(session_key)

            if not session_data is None:
                try:
                    SessionStore().decode(session_data)
                    backend.delete(session_key)
                except Error:
                    continue
