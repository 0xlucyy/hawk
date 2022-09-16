import os
import sys
import pytest
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import Flask
from unittest.mock import MagicMock, patch
from unittest import mock
from backend.models.models import ENS as ens
from config import TestConfiguration

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
        ens.query = self.SESSION.query_property()
        ens.metadata.create_all(bind=self.ENGINE)

        domain_expired = ens(
            name = 'r2-d2',
            owner = '0x770c13284eB073F07d7c88fb787c319d533F785A',
            expiration = datetime.now(),
            bids = 2,
            bids_details = "{'0': '1eth', '0': '1.22eth'}",
            listings = 0,
            listings_details = "{}"
        )

        domain_active = ens(
            name = 'tiger',
            owner = '0xcF1A4C3bE75D8E4AD112755F442433B860249C17',
            expiration = (datetime.now() + timedelta(hours=1)),
            bids = 0,
            bids_details = "{}",
            listings = 1,
            listings_details = "{'0': '10eth'}"
        )

        domain_active_1 = ens(
            name = 'ring',
            owner = '0x6b558C075Dce25A9daA5Fa2045a6b302aCb80308',
            expiration = (datetime.now() + timedelta(hours=24)),
            bids = 0,
            bids_details = "{}",
            listings = 0,
            listings_details = "{}"
        )

        domain_active_2 = ens(
            name = 'water',
            owner = '0x6b558C075Dce25A9daA5Fa2045a6b302aCb80308',
            expiration = (datetime.now() + timedelta(hours=100)),
            bids = 0,
            bids_details = "{}",
            listings = 0,
            listings_details = "{}"
        )

        self.SESSION.add(domain_expired)
        self.SESSION.add(domain_active)
        self.SESSION.add(domain_active_1)
        self.SESSION.add(domain_active_2)
        self.SESSION.commit()

    def teardown_method(self):
        self.SESSION.remove()
        ens.metadata.drop_all(bind=self.ENGINE)

    def test_new_domain(self):
        """
        Ensure that a new domain can be declared properly.
        """
        time = datetime.now()
        domain = ens(
            name = 'R2-d2',
            owner = '0xcF1A4C3bE75D8E4AD112755F442433B860249C17',
            expiration = time,
            bids = 2,
            bids_details = "{'0': '1eth', '0': '1.22eth'}",
            listings = 0,
            listings_details = "{}"
        )
        assert domain.name == 'r2-d2'
        assert domain.owner == '0xcF1A4C3bE75D8E4AD112755F442433B860249C17'
        assert domain.expiration == time
        assert domain.bids == 2
        assert domain.bids_details == "{'0': '1eth', '0': '1.22eth'}"
        assert domain.listings == 0
        assert domain.listings_details == "{}"


    def test_domain_exists(self):
        """
        Ensures that a domain can be retrieved from db
        using a domain name.
        """
        expected = 'Domain 1: r2-d2'

        # Tested function
        actual = ens.domain_exists('r2-D2')

        assert str(actual) == expected
        assert actual.owner == '0x770c13284eB073F07d7c88fb787c319d533F785A'
        assert actual.bids == 2
        assert actual.bids_details == "{'0': '1eth', '0': '1.22eth'}"
        assert actual.listings == 0
        assert actual.listings_details == "{}"

    def test_domain_exists_returns_false(self):
        """
        Ensures that a domain that does not exists in db
        returns None.
        """
        expected = False

        # Tested function
        actual = ens.domain_exists('DOES NOT EXISTS IN DB')

        assert actual == expected

    def test_expiring(self):
        """
        Ensure that only expiring domains are returned, in asc
        order.
        Notice domain r2-d2 is already expired and domain water
        expiration falls outside the 3 day window.
        """
        expected = '[Domain 2: tiger, Domain 3: ring]'

        # Tested function
        actual = ens.expiring(expires_in_days=3)

        assert str(actual) == expected
        assert len(actual) == 2
        assert actual[0].owner == '0xcF1A4C3bE75D8E4AD112755F442433B860249C17'
        assert actual[1].owner == '0x6b558C075Dce25A9daA5Fa2045a6b302aCb80308'
        assert actual[0].expiration < actual[1].expiration

    def test_expiring_in_0_days(self):
        """
        Zero domains expire in 0 days.
        """
        expected = '[]'

        # Tested function
        actual = ens.expiring(expires_in_days=0)

        assert str(actual) == expected
        assert len(actual) == 0

    def test_domains_by_expiration_asc(self):
        """
        Ensure all domains are returned by expiration in
        called order.
        """
        expected = '[Domain 1: r2-d2, Domain 2: tiger, Domain 3: ring, Domain 4: water]'

        # Tested function
        actual = ens.domains_by_expiration(order='asc')

        assert str(actual) == expected
        assert len(actual) == 4
        assert actual[0].expiration <= actual[1].expiration <= actual[2].expiration <= actual[3].expiration

    def test_domains_by_expiration_desc(self):
        """
        Ensure all domains are returned by expiration in
        called order.
        """
        expected = '[Domain 4: water, Domain 3: ring, Domain 2: tiger, Domain 1: r2-d2]'

        # Tested function
        actual = ens.domains_by_expiration(order='desc')

        assert str(actual) == expected
        assert len(actual) == 4
        assert actual[0].expiration >= actual[1].expiration >= actual[2].expiration >= actual[3].expiration