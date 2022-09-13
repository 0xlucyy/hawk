from app import db
from datetime import datetime

# https://docs.sqlalchemy.org/en/13/orm/extensions/declarative/api.html#abstract
class Lockable(db.Model):
    __abstract__ = True

    _is_locked = db.Column(db.Boolean, default=False, nullable=False)
    _locked_at = db.Column(db.TIMESTAMP)
    _last_activity_at = db.Column(db.TIMESTAMP)

    def _unlock(self):
        self._is_locked = False

    def _lock(self):
        self._is_locked = True
        self._locked_at = datetime.now()
        self._last_activity_at = datetime.now()