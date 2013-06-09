from django.contrib.sessions.backends.base import SessionBase, CreateError
from redis_sessions import backend


class SessionStore(SessionBase):
    '''
    Redis Session Backend For Django
    '''
    def __init__(self, session_key=None):
        super(SessionStore, self).__init__(session_key)

    def load(self):
        session_data = backend.get(self._get_or_create_session_key())
        if not session_data is None:
            return self.decode(session_data)
        else:
            self.create()
            return {}

    def exists(self, session_key):
        return backend.exists(session_key)

    def create(self):
        while True:
            self._session_key = self._get_new_session_key()

            try:
                self.save(must_create=True)
            except CreateError:
                continue

            self.modified = True

            return

    def save(self, must_create=False):
        session_key = self._get_or_create_session_key()

        if must_create and self.exists(session_key):
            raise CreateError

        expire = self.get_expiry_age()
        data = self.encode(self._get_session(no_load=must_create))

        backend.save(session_key, expire, data)

    def delete(self, session_key=None):
        if session_key is None:
            if self.session_key is None:
                return
            session_key = self.session_key

        backend.delete(session_key)
