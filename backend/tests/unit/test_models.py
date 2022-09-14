
import os
import sys
import pytest
from datetime import datetime

sys.path.append(os.path.abspath('./'))

from backend.models.models import ENS

# import pdb; pdb.set_trace()

def test_new_user():
    """
    """
    time = datetime.now()
    domain = ENS(
        name = 'test.eth',
        owner = '0xcF1A4C3bE75D8E4AD112755F442433B860249C17',
        expiration = time,
        bids = 2,
        bids_details = "{'0': '1eth', '0': '1.22eth'}",
        listings = 0,
        listings_details = "{}"
    )

    assert domain.name == 'test.eth'
    assert domain.owner == '0xcF1A4C3bE75D8E4AD112755F442433B860249C17'
    assert domain.expiration == time
    assert domain.bids == 2
    assert domain.bids_details == "{'0': '1eth', '0': '1.22eth'}"
    assert domain.listings == 0
    assert domain.listings_details == "{}"