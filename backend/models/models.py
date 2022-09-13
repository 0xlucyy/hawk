from app import db
from datetime import datetime
from backend.models._base import Base
from backend.models._lockable import Lockable

class ENS(Base, Lockable):
    '''  '''
    __tablename__ = 'domains'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    owner = db.Column(db.String(200))
    expiration = db.Column(db.TIMESTAMP)
    bids = db.Column(db.Integer)
    listings = db.Column(db.Integer)

    # db.relationships
    # matches = db.relationship('Match', primaryjoin="or_(Player.id==Match.player_1, Player.id==Match.player_2)", lazy='dynamic')

    def __init__(self, name: str, owner: str, expiration: datetime,
                 bids: str, listings: str):
        self.name = name
        self.owner = owner
        self.expiration = expiration
        self.bids = bids
        self.listings = listings
        self._created_at = datetime.now()
        self._updated_at = datetime.now()

    def __repr__(self):
        return f'Domain {self.id}: {self.name}'
