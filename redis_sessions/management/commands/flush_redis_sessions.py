from django.core.management.base import NoArgsCommand
from redis_sessions.connection import redis_server


class Command(NoArgsCommand):
    help = 'flush all redis sessions'

    def handle_noargs(self, **options):
        redis_server.flushdb()
