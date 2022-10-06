from app import db

# https://docs.sqlalchemy.org/en/13/orm/extensions/declarative/api.html#abstract
class Base(db.Model):
    __abstract__ = True

    _created_at = db.Column(db.TIMESTAMP, default=db.func.now())
    _updated_at = db.Column(db.TIMESTAMP, default=db.func.now(), onupdate=db.func.now())