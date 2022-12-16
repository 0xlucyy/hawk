from app import db, app
from datetime import datetime, timedelta
from backend.models._base import Base
from backend.models._lockable import Lockable
from sqlalchemy import func
from backend.utils.exceptions import (
    DomainModelDataTypeError
)
from backend.utils.utils import (
    domain_status
)
from dateutil.relativedelta import relativedelta
# import pdb; pdb.set_trace()


class Domains(Base, Lockable):
    '''  '''
    __tablename__ = 'domains'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(200), nullable=False)
    hash = db.Column(db.VARCHAR(100), unique=True, nullable=False)
    owner = db.Column(db.String(100), nullable=False)
    available = db.Column(db.Boolean, nullable=False)
    # expiration = time expiration ends.
    expiration = db.Column(db.DATETIME, nullable=True)
    # grace = time grace ends.
    grace = db.Column(db.DATETIME, nullable=True)
    # auction = time auction ends.
    auction = db.Column(db.DATETIME, nullable=True)
    status = db.Column(db.VARCHAR(50), nullable=False)

    # db.relationships
    orders = db.relationship('Orders', backref='domains') # 1 domain to many orders

    def __init__(self, name: str, owner: str, expiration: str,
                 hash: str, available: bool):
        if not isinstance(name, str):
            raise DomainModelDataTypeError(msg='Name must be a string.')
        if not isinstance(hash, str):
            raise DomainModelDataTypeError(msg='Hash must be a string.')
        if not isinstance(owner, str):
            raise DomainModelDataTypeError(msg='Owner must be a string.')
        if not isinstance(available, bool):
            raise DomainModelDataTypeError(msg='Available must be a bool.')
        if not isinstance(expiration, str): # "YYYY-MM-DD HH:MM:SS"
            raise DomainModelDataTypeError(msg='Expiration must be a datetime string.')

        self.name = name.lower()
        self.owner = owner
        self.hash = hash
        self.available = available
        self._created_at = datetime.now()
        self._updated_at = datetime.now()
        self._last_activity_at = datetime.now()

        self.expiration = datetime.strptime(
            expiration, app.config['DATETIME_STR_FORMAT']
        ) if expiration != 'null' else None
        self.grace = (self.expiration + relativedelta( \
            days=app.config['ENS_GRACE_PERIOD'])) \
            if self.expiration != None else None
        self.auction = (self.grace + relativedelta( \
            days=app.config['ENS_AUCTION_PERIOD'])) \
            if self.grace != None else None
        
        self.status = domain_status(self.expiration, self.grace, self.auction)

    def __repr__(self):
        return f'Domain {self.id}: {self.name}'

    @classmethod
    def get_times_and_status(cls, _expiration: str = None):
        '''
        Grace & Auction expirations are calculated based off
        the expiration value received from ENS_Base_Registrar
        contract, function nameExpires.
        '''
        expiration = datetime.strptime(
            _expiration, app.config['DATETIME_STR_FORMAT']
        ) if _expiration != 'null' else None
        grace = (expiration + relativedelta( \
            days=app.config['ENS_GRACE_PERIOD'])) \
            if expiration != None else None
        auction = (grace + relativedelta( \
            days=app.config['ENS_AUCTION_PERIOD'])) \
            if grace != None else None
        status = domain_status(expiration, grace, auction)
        return {'grace':grace, 'auction':auction, 'status':status}
        # return domain if domain != None else False

    @classmethod
    def domain_exists(cls, domain_name: str = None):
        '''
        If domain exists in DB, returns domain, else
        returns false.

        Returns: backend.models.models.Domains or False
        '''
        domain = cls.query.filter(
            func.lower(Domains.name) == func.lower(domain_name)
        ).first()
        return domain if domain != None else False

    @classmethod
    def expiring(cls, expires_in_days: int = 10):
        '''
        returns only expiring domains, from those expiring
        first to those expiring last.
        '''
        day = datetime.now() + timedelta(days=expires_in_days)
        domains = cls.query.filter(
            Domains.expiration <= day,
            Domains.expiration > datetime.now(),
        ).order_by(
            Domains.expiration.asc()
        ).all()
        return domains

    @classmethod
    def all_domains(cls, order='asc'):
        '''
        returns all domains, from those expiring first to
        those expiring last.
        '''
        domains = cls.query.order_by(
            Domains.expiration.asc() if order == 'asc' else Domains.expiration.desc()
        ).all()
        return domains

    @classmethod
    def expired(cls):
        '''
        returned domains which have expired but have yet
        to leave auction.
        '''
        domains = cls.query.filter(
            Domains.expiration < datetime.now(), # Expiration in past.
            Domains.auction > datetime.now() # Auction already expired.
        ).order_by(
            Domains.expiration.asc()
        ).all()
        return domains

    @classmethod
    def auctions(cls):
        '''
        After grace expiration, before 21 day auction
        '''
        domains = cls.query.filter(
            Domains.grace < datetime.now(), # Grace already expired
            Domains.auction > datetime.now() # Auction still on going
        ).order_by(
            Domains.auction.asc()
        ).all()
        return domains


class Markets(Base, Lockable):
    '''   '''
    __tablename__ = 'markets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(100), nullable=False)
    base_url = db.Column(db.VARCHAR(100), nullable=False)
    explore_url = db.Column(db.VARCHAR(100), nullable=False)
    address = db.Column(db.VARCHAR(100), nullable=True)
    notes = db.Column(db.VARCHAR(300), nullable=True)

    # db.relationships
    orders = db.relationship('Orders', backref='markets') # 1 market to many orders

    def __init__(self, name, base_url, explore_url, address, notes):
        self.name = name
        self.base_url = base_url
        self.explore_url = explore_url
        self.address = address
        self.notes = notes

    def __repr__(self):
        return f'Market {self.id}: {self.name}'

    @classmethod
    def get_market_orders(cls, name: str = None):
        '''
        returns 
        '''
        markets = cls.query.filter(Markets.name == name).first()
        return markets

    @classmethod
    def all_markets(cls, order='asc'):
        '''
        returns all markets, from those expiring first to
        those expiring last.
        '''
        # import pdb; pdb.set_trace()
        markets = cls.query.order_by(
            Markets.name.asc() if order == 'asc' else Markets.name.desc()
        ).all()
        return markets

class Orders(Base, Lockable):
    '''   '''
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    order = db.Column(db.TEXT)
    
    # db.relationships
    market_id = db.Column(db.Integer, db.ForeignKey('markets.id'))
    domain_id = db.Column(db.Integer, db.ForeignKey('domains.id'))

    def __init__(self, market_id, domain_id, order):
        self.market_id = market_id
        self.domain_id = domain_id
        self.order = order

    def __repr__(self):
        return f'Order {self.id} - Domain: {self.domain_id}'

    @classmethod
    def get_orders(cls, domain_id: int = None):
        '''
        returns 
        '''
        markets = cls.query.filter(Orders.domain_id == domain_id).all()
        return markets

    @classmethod
    def get_order_by_hash(cls, _hash: str = None):
        '''
        returns 
        '''
        # https://stackoverflow.com/a/8562155 - .has()
        orders = cls.query.filter(Orders.domains.has(hash = _hash)).all()
        #).order_by(
        #     Orders.domains.expiration.asc()
        # ).all()
        return orders

# Orders.order = {
#     'status': 'VALID',
#     'expiration': 8127638921736,
#     'listings': {'amount': 1, 'amount': .67},
#     'bids': {}
# }