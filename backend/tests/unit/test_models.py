from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import Flask
from unittest.mock import patch
from backend.models.models import Domains as domains
from backend.models.models import Markets as markets
from backend.models.models import Orders as orders
from config import TestConfiguration
from backend.utils.formatters import stringify

# import pdb; pdb.set_trace()

class TestModels():
    ENGINE = create_engine(TestConfiguration.SQLALCHEMY_DATABASE_URI)
    SESSION = scoped_session(
              sessionmaker(autocommit=False,
                           autoflush=False, bind=ENGINE))
    APP = Flask('HAWK_TESTING_MODELS')
    APP.config.from_object(TestConfiguration)

    def setup_method(self):
        self.maxDiff = None
        domains.query = self.SESSION.query_property()
        domains.metadata.create_all(bind=self.ENGINE)

        # Add 4 domains.
        domain_expired = domains(
            name = 'r2-d2',
            owner = '0x770c13284eB073F07d7c88fb787c319d533F785A',
            expiration = datetime.now(),
            hash = 2
        )
        domain_active = domains(
            name = 'tiger',
            owner = '0xcF1A4C3bE75D8E4AD112755F442433B860249C17',
            expiration = (datetime.now() + timedelta(hours=1)),
            hash = 0
        )
        domain_active_1 = domains(
            name = 'ring',
            owner = '0x6b558C075Dce25A9daA5Fa2045a6b302aCb80308',
            expiration = (datetime.now() + timedelta(hours=24)),
            hash = 2
        )
        domain_active_2 = domains(
            name = 'water',
            owner = '0x6b558C075Dce25A9daA5Fa2045a6b302aCb80308',
            expiration = (datetime.now() + timedelta(hours=100)),
            hash = 0
        )

        self.SESSION.add(domain_expired)
        self.SESSION.add(domain_active)
        self.SESSION.add(domain_active_1)
        self.SESSION.add(domain_active_2)
        self.SESSION.commit()
        
        # Add 4 markets
        market_1 = markets(name = 'looksrare')
        market_2 = markets(name = 'opensea')
        market_3 = markets(name = 'x2y2')
        market_4 = markets(name = 'ensvision')

        self.SESSION.add(market_1)
        self.SESSION.add(market_2)
        self.SESSION.add(market_3)
        self.SESSION.add(market_4)
        self.SESSION.commit()

        # Add 4 orders
        order_1 = orders(market_id = 1, domain_id = 1,
                         order = stringify({'status': 'VALID', 'expiration': 8127638921736, 'listings': {'amount': 1, 'amount': .67}, 'bids': {}}))
        order_2 = orders(market_id = 1, domain_id = 2,
                         order = stringify({'status': 'VALID', 'expiration': 8127638921736, 'listings': {'amount': .95}, 'bids': {'amount': .55}}))
        order_3 = orders(market_id = 3, domain_id = 2,
                         order = stringify({'status': 'VALID', 'expiration': 8127638921766, 'listings': {'amount': .9}, 'bids': {'amount': .6}}))
        order_4 = orders(market_id = 4, domain_id = 4,
                         order = stringify({'status': 'VALID', 'expiration': 8127638921736, 'listings': {}, 'bids': {'amount': 1, 'amount': .67}}))

        self.SESSION.add(order_1)
        self.SESSION.add(order_2)
        self.SESSION.add(order_3)
        self.SESSION.add(order_4)
        self.SESSION.commit()

    def teardown_method(self):
        self.SESSION.remove()
        domains.metadata.drop_all(bind=self.ENGINE)

    # def test_new_domain(self):
    #     """
    #     Ensure that a new domain can be declared properly.
    #     """
    #     time = datetime.now()
    #     domain = domains(
    #         name = 'R2-D2-f2',
    #         owner = '0xcF1A4C3bE75D8E4AD112755F442433B860249C17',
    #         expiration = time,
    #         hash = 2
    #     )
    #     assert domain.name == 'r2-d2-f2'
    #     assert domain.owner == '0xcF1A4C3bE75D8E4AD112755F442433B860249C17'
    #     assert domain.expiration == time
    #     assert domain.hash == 2


    # def test_domain_exists(self):
    #     """
    #     Ensures that a domain can be retrieved from db
    #     using a domain name.
    #     """
    #     expected = 'Domain 1: r2-d2'

    #     # Tested function
    #     actual = domains.domain_exists('r2-D2')

    #     assert str(actual) == expected
    #     assert actual.name == 'r2-d2'
    #     assert actual.hash == '2'
    #     assert actual.owner == '0x770c13284eB073F07d7c88fb787c319d533F785A'

    # def test_domain_exists_returns_false(self):
    #     """
    #     Ensures that a domain that does not exists in db
    #     returns None.
    #     """
    #     expected = False

    #     # Tested function
    #     actual = domains.domain_exists('DOES NOT EXISTS IN DB')

    #     assert actual == expected

    # def test_expiring(self):
    #     """
    #     Ensure that only expiring domains are returned, in asc
    #     order.
    #     Notice domain r2-d2 is already expired and domain water
    #     expiration falls outside the 3 day window.
    #     """
    #     expected = '[Domain 2: tiger, Domain 3: ring]'

    #     # Tested function
    #     actual = domains.expiring(expires_in_days=3)

    #     assert str(actual) == expected
    #     assert len(actual) == 2
    #     assert actual[0].owner == '0xcF1A4C3bE75D8E4AD112755F442433B860249C17'
    #     assert actual[1].owner == '0x6b558C075Dce25A9daA5Fa2045a6b302aCb80308'
    #     assert actual[0].expiration < actual[1].expiration

    # def test_expiring_in_0_days(self):
    #     """
    #     Zero domains expire in 0 days.
    #     """
    #     expected = '[]'

    #     # Tested function
    #     actual = domains.expiring(expires_in_days=0)

    #     assert str(actual) == expected
    #     assert len(actual) == 0

    # def test_domains_by_expiration_asc(self):
    #     """
    #     Ensure all domains are returned by expiration in
    #     called order.
    #     """
    #     expected = '[Domain 1: r2-d2, Domain 2: tiger, Domain 3: ring, Domain 4: water]'

    #     # Tested function
    #     actual = domains.domains_by_expiration(order='asc')

    #     assert str(actual) == expected
    #     assert len(actual) == 4
    #     assert actual[0].expiration <= actual[1].expiration <= actual[2].expiration <= actual[3].expiration

    # def test_markets_available(self):
    #     """
    #     Ensure all markets are returned correctly.
    #     """
    #     expected = '[Market 1: looksrare, Market 2: opensea, Market 3: x2y2, Market 4: ensvision]'
        
    #     # Tested function
    #     actual = markets.query.all()

    #     assert str(actual) == expected
    #     assert len(actual) == 4

    def test_market_orders(self):
        """
        Ensure model returns all orders of a single market.
        """
        expected_orders = '[Order 1 - Domain: 1, Order 2 - Domain: 2]'
        expected_order_1 = '{"status": "VALID", "expiration": 8127638921736, "listings": {"amount": 0.67}, "bids": {}}'
        expected_order_2 = '{"status": "VALID", "expiration": 8127638921736, "listings": {"amount": 0.95}, "bids": {"amount": 0.55}}'
        expected_market = 'Market 1: looksrare'
        exppected_domain_1 = 1 # r2-d2
        exppected_domain_2 = 2 # tiger
        exppected_market_id = 1 # looksrare
        
        # Tested function
        actual = markets.get_market_orders(name='looksrare')

        import pdb; pdb.set_trace()

        assert str(actual.orders) == expected_orders
        assert len(actual.orders) == 2
        assert str(actual) == expected_market
        assert actual.orders[0].order == expected_order_1
        assert actual.orders[1].order == expected_order_2
        assert actual.orders[0].domain_id == exppected_domain_1
        assert actual.orders[1].domain_id == exppected_domain_2
        assert actual.orders[0].market_id == exppected_market_id
        assert actual.orders[1].market_id == exppected_market_id