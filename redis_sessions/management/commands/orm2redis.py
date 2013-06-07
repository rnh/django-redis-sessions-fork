from django.core.management.base import NoArgsCommand
from django.utils import timezone
from django.contrib.sessions.models import Session
from redis_sessions import utils


class Command(NoArgsCommand):
    help = 'copy django orm sessions to redis'

    def handle_noargs(self, **options):
        now = timezone.now()

        for session in Session.objects.filter(
            expire_date__gt=now
        ):
            expire = session.expire_date - now
            expire = expire.seconds + expire.days * 86400

            utils.set(
                utils.session_key(session.session_key),
                expire,
                utils.force_unicode(session.session_data)
            )
