from django.contrib.sessions.backends.base import SessionBase, CreateError
from redis_sessions import utils


class SessionStore(SessionBase):
    """
    Implements Redis database session store.
    """
    def __init__(self, session_key=None):
        super(SessionStore, self).__init__(session_key)

    def load(self):
        try:
            session_data = utils.get(
                utils.session_key(
                    self._get_or_create_session_key()
                )
            )
            return self.decode(
                utils.force_unicode(session_data)
            )
        except:
            self.create()

            return {}

    def exists(self, session_key):
        return utils.exists(
            utils.session_key(session_key)
        )

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

        key = utils.session_key(session_key)
        expire = self.get_expiry_age()
        data = self.encode(
            self._get_session(no_load=must_create)
        )

        utils.set(key, expire, data)

    def delete(self, session_key=None):
        if session_key is None:
            if self.session_key is None:
                return
            session_key = self.session_key
        try:
            utils.delete(
                utils.session_key(session_key)
            )
        except:
            pass
