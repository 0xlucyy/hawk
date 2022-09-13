
import os
import sys
import pytest
from datetime import datetime

sys.path.append(os.path.abspath('./'))

from backend.models.models import ENS


def test_new_user():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, hashed_password, and role fields are defined correctly
    """
    time = datetime.now()
    domain = ENS(name = 'test.eth',
                 owner = '0xcF1A4C3bE75D8E4AD112755F442433B860249C17',
                 expiration = time,
                 bids = 2,
                 listings = 0)
    # import pdb; pdb.set_trace()
    assert domain.name == 'test.eth'
    assert domain.owner == '0xcF1A4C3bE75D8E4AD112755F442433B860249C17'
    assert domain.expiration == time
    assert domain.bids == 2
    assert domain.listings == 0