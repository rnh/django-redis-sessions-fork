from django.core.management.base import NoArgsCommand
from django.utils import timezone
from django.contrib.sessions.models import Session
from redis_sessions import backend


class Command(NoArgsCommand):
    help = 'copy django orm sessions to redis'

    def handle_noargs(self, **options):
        now = timezone.now()

        sessions = Session.objects.filter(expire_date__gt=now)
        count = sessions.count()
        counter = 1

        self.stdout.write('sessions to copy %d\n' % count)

        for session in sessions:
            self.stdout.write('processing %d of %d\n' % (counter, count))

            backend.delete(session.session_key)

            expire = session.expire_date - now
            expire = expire.seconds + expire.days * 86400

            backend.save(
                session.session_key,
                expire,
                session.session_data
            )

            counter += 1
