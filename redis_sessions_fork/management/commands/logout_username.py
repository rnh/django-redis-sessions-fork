from binascii import Error

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from ...session import SessionStore
from ... import backend


class Command(BaseCommand):
    args = '<username username ...>'
    help = 'Log out users by deleting their session(s) in redis session store.'

    def handle(self, *args, **kwargs):
        verbosity = int(kwargs.get('verbosity', 1))
        for username in args:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                if verbosity >= 0:
                    print "No user with username", username, "exists"
                continue

            if verbosity >= 1:
                print "Logging out", user

            session_keys = backend.keys('*')
            num_keys_before = len(session_keys)
            if verbosity >= 3: 
                print "Number of session keys before", num_keys_before
            for session_key in session_keys:
                session_data = backend.get(session_key)

                if not session_data is None:
                    try:
                        dec = SessionStore().decode(session_data)
                        if dec.get('_auth_user_id') == user.id:
                            if verbosity >= 2: 
                                print "Removing session", session_key, dec
                            backend.delete(session_key)
                    except (Error, TypeError):
                        continue
            session_keys = backend.keys('*')
            num_keys_after = len(session_keys)
            if verbosity >= 3:
                print "Number of session keys after", num_keys_after
            if verbosity >= 1: 
                print "Deleted", num_keys_before - num_keys_after, \
                        "session(s) for", user
                print ""
