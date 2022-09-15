from app import db
from datetime import datetime, timedelta
from backend.models._base import Base
from backend.models._lockable import Lockable
from sqlalchemy import func

class ENS(Base, Lockable):
    '''  '''
    __tablename__ = 'domains'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    owner = db.Column(db.String(200))
    expiration = db.Column(db.TIMESTAMP)
    bids = db.Column(db.Integer)
    bids_details = db.Column(db.String(300))
    listings = db.Column(db.Integer)
    listings_details = db.Column(db.String(300))

    # db.relationships
    # matches = db.relationship('Match', primaryjoin="or_(Player.id==Match.player_1, Player.id==Match.player_2)", lazy='dynamic')

    def __init__(self, name: str, owner: str, expiration: datetime,
                 bids: int, listings: int, bids_details: str,
                 listings_details: str):
        self.name = name.lower()
        self.owner = owner
        self.expiration = expiration
        self.bids = bids
        self.bids_details = bids_details
        self.listings = listings
        self.listings_details = listings_details
        self._created_at = datetime.now()
        self._updated_at = datetime.now()

    def __repr__(self):
        return f'Domain {self.id}: {self.name}'
    
    @classmethod
    def domain_exists(cls, domain_name: str = None):
        '''
        If domain exists in DB, returns domain, else
        returns false.

        Returns: backend.models.models.ENS or False
        '''
        domain = cls.query.filter(
            func.lower(ENS.name) == func.lower(domain_name)
        ).first()
        return domain if domain != None else False

    @classmethod
    def expiring(cls, expires_in_days: int = None):
        '''
        returns only expiring domains, from those expiring
        first to those expiring last.
        '''
        day = datetime.now() + timedelta(days=expires_in_days)
        domains = cls.query.filter(
            ENS.expiration <= day,
            ENS.expiration > datetime.now(),
        ).order_by(
            ENS.expiration.asc()
        ).all()
        return domains

    @classmethod
    def domains_by_expiration(cls, order: str = 'asc'):
        '''
        returns domains from those expiring first to those
        expiring last.
        '''
        if order != 'asc' and order != 'desc':
            return []
        domains = cls.query.filter(
            ENS.expiration
        ).order_by(
            ENS.expiration.asc() if order == 'asc' else ENS.expiration.desc()
        ).all()
        return domains